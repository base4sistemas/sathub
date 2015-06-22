# -*- coding: utf-8 -*-
#
# sathub/custom.py
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

from flask.ext.restful import reqparse

from .comum.util import NUM_CAIXA_MIN
from .comum.util import NUM_CAIXA_MAX


def numero_caixa(value, name):
    numero = int(value)
    if NUM_CAIXA_MIN <= numero <= NUM_CAIXA_MAX:
        return numero
    raise ValueError('Parametro {} nao indica um numero de caixa '
            'valido: {}'.format(name, value))


parser = reqparse.RequestParser()

parser.add_argument('numero_caixa',
        type=numero_caixa,
        required=True,
        location=['headers', 'values'],
        help=u'O número do caixa de onde a solicitação partiu')


def request_parser():
    global parser
    return parser.copy()
