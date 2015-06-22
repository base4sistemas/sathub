# -*- coding: utf-8 -*-
#
# sathub/resources/trocarcodigodeativacao.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
    Este método permite a troca do código de ativação, que é uma senha,
    nomalmente definida pelo contribuinte proprietário do equipamento SAT.

    Se o código de ativação original tiver sido perdido, então o código de
    ativação de emergência deverá ser escrito no arquivo de configurações e
    deverá ser usada a opção ``2`` para que seja reconhecido pelo equipamento
    SAT como o código de ativação de emergência.

    Será muito mais prático usar o software de gerenciamento do fabricante para
    efetuar a troca do código de ativação, a menos que o estabelecimento siga
    uma política de troca frequente do código de ativação devido a questões de
    segurança. Neste caso, seria muito mais interessante implementar esta
    funcionalidade na aplicação de retaguarda, já que é uma operação puramente
    administrativa. Mas isso é apenas uma sugestão.
"""

import logging

from flask import abort
from flask.ext import restful

from ..comum.util import hexdump
from ..comum.util import instanciar_funcoes_sat
from ..custom import request_parser


logger = logging.getLogger('sathub.resource')


def opcao_codigo(value, name):
    # 1 - codigo de ativação normal
    # 2 - código de ativação de emergência
    opcao = int(value)
    if opcao not in [1, 2]: # FIXME: deveriam ser constantes em `satcomum`
        raise ValueError('Parametro {} invalido: {}'.format(name, value))
    return opcao


parser = request_parser()

parser.add_argument('opcao',
        type=opcao_codigo,
        required=True,
        help=u'Identifica a que se refere o código de ativação usado '
                u'para realizar a troca')

parser.add_argument('novo_codigo',
        type=str,
        required=True,
        help=u'Novo código de ativação')

parser.add_argument('novo_codigo_confirmacao',
        type=str,
        required=True,
        help=u'Confirmação do novo código de ativação')


class TrocarCodigoDeAtivacao(restful.Resource):

    def post(self):
        args = parser.parse_args()

        numero_caixa = args['numero_caixa']
        opcao = args['opcao']
        novo_codigo = args['novo_codigo']
        novo_codigo_confirmacao = args['novo_codigo_confirmacao']

        abort(501) # FIXME: consultar número de sessão não implementado
        # 501 - Server does not recognise method or lacks ability to fulfill
        # NOTE: https://github.com/base4sistemas/satcfe

        fsat = instanciar_funcoes_sat(numero_caixa)
        retorno = fsat.trocar_codigo_ativacao(
                opcao,
                novo_codigo,
                novo_codigo_confirmacao)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Retorno "TrocarCodigoDeAtivacao" ('
                    'numero_caixa={!r}, opcao={!r}, novo_codigo={!r}, '
                    'novo_codigo_confirmacao={!r})\n{}'.format(
                            numero_caixa,
                            opcao,
                            novo_codigo,
                            novo_codigo_confirmacao,
                            hexdump(retorno)))

        return dict(funcao='TrocarCodigoDeAtivacao', retorno=retorno)
