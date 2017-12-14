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
from ..comum.util import instanciar_funcoes_sat
from ..custom import request_parser


logger = logging.getLogger('sathub.resource')

parser = request_parser()

parser.add_argument('dados_venda',
        type=str,
        required=True,
        help=u'XML contendo os dados do CF-e de venda')


class EnviarPagamento(restful.Resource):

    def post(self):
        args = parser.parse_args()

        numero_caixa = args['numero_caixa']
        chave_requisicao = args['chave_requisicao']
        estabecimento = args['estabecimento']
        serial_pos = args['serial_pos']
        cpnj = args['cpnj']
        icms_base = args['icms_base']
        vr_total_venda = args['vr_total_venda']
        id_fila_validador = args['id_fila_validador']
        h_multiplos_pagamentos = args['h_multiplos_pagamentos']
        h_anti_fraude = args['h_anti_fraude']
        cod_moeda = args['cod_moeda']
        origem_pagemento = args['origem_pagemento']

        fsat = instanciar_funcoes_sat(numero_caixa)
        retorno = fsat.enviar_pagamento(
            chave_requisicao, estabecimento, serial_pos, cpnj, icms_base,
            vr_total_venda, id_fila_validador, h_multiplos_pagamentos,
            h_anti_fraude,cod_moeda, origem_pagemento
        )

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Retorno "EnviarPagamento" '
                    '(numero_caixa=%s)\n%s', numero_caixa, hexdump(retorno))

        return dict(funcao='EnviarPagamento', retorno=retorno)
