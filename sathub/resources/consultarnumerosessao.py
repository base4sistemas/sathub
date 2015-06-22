# -*- coding: utf-8 -*-
#
# sathub/resources/consultarnumerosessao.py
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

import logging

from flask import abort
from flask.ext import restful

from ..comum.util import hexdump
from ..comum.util import instanciar_funcoes_sat
from ..custom import request_parser


logger = logging.getLogger('sathub.resource')

parser = request_parser()

parser.add_argument('numero_sessao',
        type=str,
        required=True,
        help=u'Número da sessão a ser consultada')


class ConsultarNumeroSessao(restful.Resource):

    def post(self):
        args = parser.parse_args()

        numero_caixa = args['numero_caixa']
        numero_sessao = args['numero_sessao']

        abort(501) # FIXME: consultar número de sessão não implementado
        # 501 - Server does not recognise method or lacks ability to fulfill
        # NOTE: https://github.com/base4sistemas/satcfe

        fsat = instanciar_funcoes_sat(numero_caixa)
        retorno = fsat.consultar_numero_sessao(numero_sessao)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Retorno "ConsultarNumeroSessao" '
                    '(numero_caixa=%s, numero_sessao=%s)\n%s',
                    numero_caixa, numero_sessao, hexdump(retorno))

        return dict(funcao='ConsultarNumeroSessao', retorno=retorno)
