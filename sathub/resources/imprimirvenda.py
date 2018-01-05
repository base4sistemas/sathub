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
from satextrato.venda import ExtratoCFeVenda

from ..comum.util import hexdump
from ..comum.util import instanciar_impressora
from ..custom import request_parser
import base64
import StringIO

from satextrato.config import conf

conf.code128_quebrar = True
conf.nota_rodape.esquerda = 'https://kmee.com.br'
conf.nota_rodape.direita = 'KMEE INFORMATICA LTDA'
conf.avancar_linhas = 3
conf.colunas.condensado = 56
conf.colunas.expandido = 23
conf.colunas.normal = 47
conf.exibir_nome_consumidor = True

logger = logging.getLogger('sathub.resource')

parser = request_parser()

parser.add_argument('dados_venda',
        type=str,
        required=True,
        help=u'XML contendo os dados do CF-e de venda')
parser.add_argument('modelo', type=str, required=True)
parser.add_argument('conexao', type=str, required=True)


class ImprimirVenda(restful.Resource):

    def post(self):
        args = parser.parse_args()

        dados_venda = args['dados_venda']
        modelo = args['modelo']
        conexao = args['conexao']

        impressora = instanciar_impressora('file', modelo, conexao)

        xml = StringIO.StringIO(base64.b64decode(dados_venda))

        impressao = ExtratoCFeVenda(xml, impressora)
        impressao.imprimir()
