# -*- coding: utf-8 -*-
#
# sathub/forms.py
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

from flask_wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators


LOCALES = ['pt_BR', 'pt']


class LoginForm(Form):

    username = StringField(u'Nome de Usuário',
            validators=[
                    validators.required(),
                    validators.length(min=2, max=20),])

    password = PasswordField('Senha',
            validators=[
                    validators.required(),
                    validators.length(min=6, max=20),])

    class Meta:
        locales = LOCALES


class EmptyForm(Form):
    class Meta:
        locales = LOCALES
