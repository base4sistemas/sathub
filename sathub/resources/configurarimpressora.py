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

from ..comum.util import instanciar_impressora
from ..custom import request_parser


logger = logging.getLogger('sathub.resource')

parser = request_parser()

parser.add_argument('configuracao_impressora',
        type=str,
        required=True,
        help=u'XML contendo a configuracao da impressora')


class ConfigurarImpressora(restful.Resource):

    def post(self):
        # args = parser.parse_args()
        #
        # configuracao_impressora = args['configuracao_impressora']
        #
        # configuracao_impressora = {'tipo_conexao': 'file',
        #                            'marca': 'elgin',
        #                            'modelo': 'i9',
        #                            'string_conexao': '/dev/usb/lp0'
        #                            }

        impressora = instanciar_impressora('file', 'elgin', 'i9','/dev/usb/lp0')
        retorno = impressora.init()

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Retorno "ConfigurarImpressora" '
                         '(conexao_impressora=%s)', retorno)

        return dict(funcao='ConfigurarImpressora', retorno=retorno)
