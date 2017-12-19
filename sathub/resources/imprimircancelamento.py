# -*- coding: utf-8 -*-
#
# sathub/resources/imprimirvenda.py
#
# Copyright 2017 KMEE INFORMATICA LTDA
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
from satextrato.cancelamento import ExtratoCFeCancelamento

from ..comum.util import hexdump
from ..comum.util import instanciar_impressora
from ..custom import request_parser
import base64
import StringIO


logger = logging.getLogger('sathub.resource')

parser = request_parser()

parser.add_argument('dados_venda',
        type=str,
        required=True,
        help=u'XML contendo os dados do CF-e de venda')
parser.add_argument('dados_cancelamento',
        type=str,
        required=True,
        help=u'XML contendo os dados do CF-e de cancelamento')
parser.add_argument('modelo', type=str, required=True)
parser.add_argument('conexao', type=str, required=True)


class ImprimirCancelamento(restful.Resource):

    def post(self):
        args = parser.parse_args()

        dados_venda = args['dados_venda']
        dados_cancelamento = args['dados_cancelamento']
        modelo = args['modelo']
        conexao = args['conexao']

        impressora = instanciar_impressora('file', modelo, conexao)

        xml_venda = StringIO.StringIO(base64.b64decode(dados_venda))
        xml_cancelamento = StringIO.StringIO(
            base64.b64decode(dados_cancelamento)
        )

        impressao = ExtratoCFeCancelamento(
            xml_venda,
            xml_cancelamento,
            impressora
        )
        impressao.imprimir()
