# -*- coding: utf-8 -*-
#
# sathub/comum/config.py
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

import json
import logging
import os
import sys

from unidecode import unidecode

import satcomum.constantes


_CONF_DEBUG = 'debug'
_CONF_CAMINHO_DLL = 'caminho_dll'
_CONF_CONVENCAO_CHAMADA = 'convencao_chamada'
_CONF_CODIGO_ATIVACAO = 'codigo_ativacao'
_CONF_USUARIO = 'usuario'
_CONF_SENHA = 'senha'


_PADRAO_DEBUG = True
_PADRAO_CAMINHO_DLL = 'sat.dll'
_PADRAO_CONVENCAO_CHAMADA = satcomum.constantes.WINDOWS_STDCALL
_PADRAO_CODIGO_ATIVACAO = '123456789'
_PADRAO_USUARIO = 'sathub'
_PADRAO_SENHA = 'sathub'


CONFIGURACAO_PADRAO = {
        _CONF_DEBUG: _PADRAO_DEBUG,
        _CONF_CAMINHO_DLL: _PADRAO_CAMINHO_DLL,
        _CONF_CONVENCAO_CHAMADA: _PADRAO_CONVENCAO_CHAMADA,
        _CONF_CODIGO_ATIVACAO: _PADRAO_CODIGO_ATIVACAO,
        _CONF_USUARIO: _PADRAO_USUARIO,
        _CONF_SENHA: _PADRAO_SENHA,
    }


class Configuracoes(object):

    def __init__(self):
        super(Configuracoes, self).__init__()

        self.pasta_projeto = os.path.abspath(os.path.join(
                os.path.abspath(os.path.dirname(__file__)), '..', '..'))

        self.arquivo = os.path.join(self.pasta_projeto, 'conf.json')
        self.debug = _PADRAO_DEBUG
        self.caminho_dll = _PADRAO_CAMINHO_DLL
        self.convencao_chamada = _PADRAO_CONVENCAO_CHAMADA
        self.codigo_ativacao = _PADRAO_CODIGO_ATIVACAO
        self.usuario = _PADRAO_USUARIO
        self.senha = _PADRAO_SENHA

        self._carregar()
        self._configurar_log()


    @property
    def nome_convencao_chamada(self):
        return [s for v,s in satcomum.constantes.CONVENCOES_CHAMADA \
                        if v == self.convencao_chamada][0]


    @property
    def is_biblioteca_existente(self):
        return os.path.isfile(self.caminho_dll)


    def _carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r') as f:
                dados = json.load(f)
        else:
            dados = CONFIGURACAO_PADRAO
            # salva um arquivo de configurações para que possa ser editado
            with open(self.arquivo, 'w') as f:
                f.write(json.dumps(CONFIGURACAO_PADRAO, indent=4))

        self.debug = dados.get(_CONF_DEBUG, _PADRAO_DEBUG)
        self.codigo_ativacao = dados.get(
                _CONF_CODIGO_ATIVACAO, _PADRAO_CODIGO_ATIVACAO)

        self.caminho_dll = dados.get(_CONF_CAMINHO_DLL, _PADRAO_CAMINHO_DLL)
        self.caminho_dll = os.path.expanduser(
                self.caminho_dll.replace('/', os.path.sep))

        self.convencao_chamada = dados.get(
                _CONF_CONVENCAO_CHAMADA, _PADRAO_CONVENCAO_CHAMADA)

        _convencoes = [v for v,s in satcomum.constantes.CONVENCOES_CHAMADA]
        if self.convencao_chamada not in _convencoes:
            raise ValueError('Valor inesperado para convencao de '
                    'chamada: {}'.format(self.convencao_chamada))

        self.usuario = dados.get(_CONF_USUARIO, _PADRAO_USUARIO)
        self.senha = dados.get(_CONF_SENHA, _PADRAO_SENHA)


    def _configurar_log(self):
        filename = os.path.join(self.pasta_projeto, 'sathub.log')

        handler = logging.FileHandler(filename)
        handler.setFormatter(
                logging.Formatter('%(asctime)s %(levelname)-8s [%(name)s] '
                        '(%(module)s:%(lineno)d) %(message)s'))

        level = logging.DEBUG if self.debug else logging.WARNING

        for name in ['flask', 'sathub',]:
            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.addHandler(handler)


    def descrever(self):
        """
        Descreve as configurações na saída padrão ou no terminal, se houver um.
        """
        import sathub

        _verbose(u'SATHub versão {}', sathub.__version__)
        _verbose(u'[-] Debug está {}', 'LIGADO' if self.debug else 'DESLIGADO')
        _verbose(u'[-] Caminho para DLL: {}', self.caminho_dll)
        _verbose(u'[-] Convenção de chamada para DLL: {}',
                self.nome_convencao_chamada)

        if not self.is_biblioteca_existente:
            _verbose(u'** DLL NÃO ENCONTRADA **')

        _verbose(u'')


conf = Configuracoes()


def _verbose(message, *args):
    as_ascii = lambda s: unidecode(s) if isinstance(s, unicode) else s

    msg = message
    if args:
        msg = message.format(*args)

    if sys.stdout.isatty():
        sys.stdout.write('{}\n'.format(as_ascii(msg)))
        sys.stdout.flush()
    else:
        # requer "WSGIRestrictStdout Off"
        # https://code.google.com/p/modwsgi/wiki/DebuggingTechniques
        # https://code.google.com/p/modwsgi/wiki/ConfigurationDirectives#WSGIRestrictStdout
        if msg:
            print >> sys.stdout, 'SATHub: {}'.format(as_ascii(msg))
