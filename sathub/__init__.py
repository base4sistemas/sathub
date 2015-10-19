# -*- coding: utf-8 -*-
#
# sathub/__init__.py
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

import base64
import os

__version__ = '0.3'

from sathub.comum.config import conf
conf.descrever()

from flask import Flask

app = Flask(__name__)
app.debug = conf.is_debug
app.secret_key = os.environ.get('SATHUB_SECRET_KEY') or \
        base64.b64encode('Nullum secretum est ubi regnat ebrietas')

import sathub.api
import sathub.views
