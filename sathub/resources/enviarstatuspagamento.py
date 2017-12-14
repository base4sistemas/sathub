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


class EnviarStatusPagamento(restful.Resource):

    def post(self):
        args = parser.parse_args()

        numero_caixa = args['numero_caixa']
        codigo_autorizacao = args['codigo_autorizacao']
        bin = args['bin']
        dono_cartao = args['dono_cartao']
        data_expiracao = args['data_expiracao']
        instituicao_financeira = args['instituicao_financeira']
        parcelas = args['parcelas']
        codigo_pagamento = args['codigo_pagamento']
        valor_pagamento = args['valor_pagamento']
        id_fila = args['id_fila']
        tipo = args['tipo']
        ultimos_quatro_digitos = args['ultimos_quatro_digitos']

        fsat = instanciar_funcoes_sat(numero_caixa)
        retorno = fsat.enviar_pagamento(
            codigo_autorizacao, bin, dono_cartao,
            data_expiracao, instituicao_financeira, parcelas,
            codigo_pagamento, valor_pagamento, id_fila,
            tipo, ultimos_quatro_digitos
        )

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Retorno "EnviarStatusPagamento" '
                    '(numero_caixa=%s)\n%s', numero_caixa, hexdump(retorno))

        return dict(funcao='EnviarStatusPagamento', retorno=retorno)