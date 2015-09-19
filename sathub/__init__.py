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

__version__ = '0.2'

from sathub.comum.config import conf as sathubconf
from satcfe import conf as satcfeconf

satcfeconf.codigo_ativacao = sathubconf.codigo_ativacao
sathubconf.descrever()

from flask import Flask

app = Flask(__name__)
app.secret_key = 'GTkjQdFVtRbmQpc0CoUAFiBUCSpLujtd'
app.debug = sathubconf.debug

import sathub.api
import sathub.views
