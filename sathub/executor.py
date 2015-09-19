# -*- coding: utf-8 -*-
#
# sathub/executor.py
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

import sys
import traceback

from unidecode import unidecode

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaSAT

from . import app
from .comum import util


CAIXA = 999


class ResultadoFuncao(object):

    def __init__(self, funcao, resposta=None):
        self.funcao = funcao
        self.resposta = resposta
        self._exc_info = sys.exc_info()

        if not self.resposta:
            if self.exc_type == ExcecaoRespostaSAT:
                self.resposta = self.exc_value


    @property
    def sucesso(self):
        if self.exc_type:
            return False
        return True


    @property
    def exc_type(self):
        return self._exc_info[0]


    @property
    def exc_value(self):
        return self._exc_info[1]


    @property
    def exc_traceback(self):
        return self._exc_info[2]


    @property
    def traceback(self):
        if self.exc_traceback:
            return ''.join(traceback.format_exception(
                    self.exc_type, self.exc_value, self.exc_traceback))
        return ''



def _executar(funcao, metodo, *args, **kwargs):
    try:
        cliente = util.instanciar_cliente_local(CAIXA)
        resposta = getattr(cliente, metodo)(*args, **kwargs)
        return ResultadoFuncao(funcao, resposta=resposta)

    except ErroRespostaSATInvalida as einv:
        app.logger.exception('Erro executando "%s"', funcao)
        return ResultadoFuncao(funcao)

    except ExcecaoRespostaSAT as exc_resp:
        app.logger.exception('Erro executando "%s"', funcao)
        return ResultadoFuncao(funcao)

    except Exception as exc:
        app.logger.exception('Erro executando "%s"', funcao)
        return ResultadoFuncao(funcao)


def consultarsat(form):
    return _executar('ConsultarSAT', 'consultar_sat')


def consultarstatusoperacional(form):
    return _executar('ConsultarStatusOperacional',
            'consultar_status_operacional')


def extrairlogs(form):
    resultado = _executar('ExtrairLogs', 'extrair_logs')
    if resultado.sucesso: # (!) alerta para 'quick fix'
        resultado.conteudo_log = unidecode(resultado.resposta.conteudo())
    return resultado
