# -*- coding: utf-8 -*-
#
# sathub/views.py
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

import collections
import platform

import flask

from flask import abort
from flask import flash
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for

from flask.ext.login import LoginManager
from flask.ext.login import UserMixin
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import login_required
from flask.ext.login import logout_user

from . import __version__ as sathub_version
from . import app
from . import executor
from . import sathubconf
from .forms import EmptyForm
from .forms import LoginForm


FUNCOES_ABERTAS = {
        'consultarsat': dict(
                titulo=u'Consultar SAT',
                descricao=u'Testa a comunicação com o equipamento SAT',
                funcao='ConsultarSAT'),

        'consultarstatusoperacional': dict(
                titulo=u'Status Operacional',
                descricao=u'Consulta o status operacional do equipamento SAT',
                funcao='ConsultarStatusOperacional'),
    }


FUNCOES_RESTRITAS = {
        'extrairlogs': dict(
                titulo=u'Extrair Logs',
                descricao=u'Obtém os registros de log do equipamento SAT.',
                funcao='ExtrairLogs'),
    }


class User(UserMixin):

    @staticmethod
    def get(user_id):
        if sathubconf.usuario != user_id:
            return None
        user = User()
        user.id = sathubconf.usuario
        return user


    @staticmethod
    def authenticate(username, password):
        if sathubconf.usuario == username:
            if sathubconf.senha == password:
                user = User()
                user.id = sathubconf.usuario
                return user
        return None


login_manager = LoginManager()
login_manager.init_app(app)


@app.context_processor
def injetar_extrainfo():
    return dict(
            sathubconf=sathubconf,
            flask_version=flask.__version__,
            python_version=platform.python_version(),
            platform_uname=' | '.join(platform.uname()),
            produto=dict(nome='SATHub', versao=sathub_version))


@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template('404.html'), 404


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('401.html'), 401


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user)
            flash('Login realizado com sucesso.', 'success')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            form.username.errors.append('athentication error')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'Você acabou de fazer o logout.', 'info')
    return redirect(url_for('index'))


@app.route('/exec/<funcaosat>', methods=['GET', 'POST'])
def executar_funcao_sat(funcaosat):

    resultado = None

    if funcaosat in FUNCOES_RESTRITAS:
        if not current_user.is_authenticated:
            return app.login_manager.unauthorized()
        funcao = FUNCOES_RESTRITAS.get(funcaosat)
    else:
        funcao = FUNCOES_ABERTAS.get(funcaosat)
        if not funcao:
            abort(404)

    form = funcao.get('form_class', EmptyForm)(request.form)
    if request.method == 'POST' and form.validate():
        resultado = getattr(executor, funcao.get('funcao').lower())(form)

    return render_template('funcao.html',
            funcao=funcao,
            form=form,
            resultado=resultado)
