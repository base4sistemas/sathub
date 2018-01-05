# -*- coding: utf-8 -*-
#
# sathub/resources/enviardadosvenda.py
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

from flask.ext import restful

from ..comum.util import hexdump
from ..comum.util import instanciar_funcoes_vfpe
from ..custom import request_parser


logger = logging.getLogger('sathub.resource')

parser = request_parser()

parser.add_argument('chave_requisicao', type=str, required=True)
parser.add_argument('estabelecimento', type=int, required=True)
parser.add_argument('serial_pos', type=str, required=True)
parser.add_argument('cnpjsh', type=str, required=True)
parser.add_argument('bc_icms_proprio', type=str, required=True)
parser.add_argument('valor', type=str, required=True)
parser.add_argument('id_fila_validador', type=str, required=True)
parser.add_argument('multiplos_pag', type=str, required=True)
parser.add_argument('anti_fraude', type=str, required=True)
parser.add_argument('moeda', type=str, required=True)
parser.add_argument('origem_pagamento', type=str, required=True)
parser.add_argument('chave_acesso_validador', type=str, required=True)
parser.add_argument('caminho_integrador',
        type=str,
        required=False,
        help=u'Caminho do integrador da MFe')


class EnviarPagamento(restful.Resource):

    def post(self):
        args = parser.parse_args()

        numero_caixa = args['numero_caixa']
        chave_requisicao = args['chave_requisicao']
        chave_acesso_validador = args['chave_acesso_validador']
        estabecimento = args['estabelecimento']
        serial_pos = args['serial_pos']
        cpnj = args['cnpjsh']
        icms_base = args['bc_icms_proprio']
        vr_total_venda = args['valor']
        id_fila_validador = args['id_fila_validador']
        h_multiplos_pagamentos = args['multiplos_pag']
        h_anti_fraude = args['anti_fraude']
        cod_moeda = args['moeda']
        origem_pagemento = args['origem_pagamento']

        if args.get('caminho_integrador'):
            fvfpe = instanciar_funcoes_vfpe(
                numero_caixa, chave_acesso_validador,
                args['caminho_integrador']
            )
        else:
            fvfpe = instanciar_funcoes_vfpe(numero_caixa)
        retorno = fvfpe.enviar_pagamento(
            chave_requisicao, estabecimento, serial_pos, cpnj, icms_base,
            vr_total_venda, id_fila_validador, h_multiplos_pagamentos,
            h_anti_fraude,cod_moeda, origem_pagemento
        )

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Retorno "EnviarPagamento" '
                    '(numero_caixa=%s)\n%s', numero_caixa, hexdump(retorno))

        return dict(funcao='EnviarPagamento', retorno=retorno)
