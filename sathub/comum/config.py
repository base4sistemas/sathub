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

import collections
import json
import logging
import os
import sys

from logging.config import dictConfig

from cerberus import Validator

from unidecode import unidecode

import satcomum.constantes


PROJECT_ROOT = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..')


DEFAULT_LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
                'verbose': {
                        'format': '%(asctime)s %(levelname)-8s [%(name)s] '\
                                        '(%(module)s:%(lineno)d) %(message)s'
                    },
                'simple': {
                        'format': '%(levelname)-8s [%(name)s] %(message)s'
                    }
            },
        'filters': {},
        'handlers': {
                'null': {
                        'level':'DEBUG',
                        'class':'logging.NullHandler',
                    },
                'console':{
                        'level':'DEBUG',
                        'class':'logging.StreamHandler',
                        'formatter': 'simple'
                    },
                'socket': {
                        'level': 'WARNING',
                        'class': 'logging.handlers.SocketHandler',
                        'host': '10.0.0.1',
                        'port': 7007
                    }
        },
        'loggers': {
                'flask': {
                        'handlers': ['null'],
                        'propagate': True,
                        'level':'INFO'
                    },
                'satcfe': {
                        'handlers': ['socket'],
                        'propagate': True,
                        'level': 'WARNING'
                    },
                'sathub': {
                        'handlers': ['socket'],
                        'level': 'WARNING',
                        'propagate': False
                    }
            }
    }


DEFAULT_CONFIG = {
        'debug': True,
        'usuario': 'sathub',
        'senha': 'sathub',
        'endpoints': [
                {
                        'alias': '900000001',
                        'descricao': 'Equipamento SAT 1',
                        'codigo_ativacao': '12345678',
                        'caminho_biblioteca': '/opt/fabricante/libsat.so',
                        'convencao_chamada': satcomum.constantes.STANDARD_C,
                },
            ]
    }


EndpointBase = collections.namedtuple('EndpointBase',
        'alias descricao codigo_ativacao caminho_biblioteca convencao_chamada')


class Endpoint(EndpointBase):

    __slots__ = ()


    @property
    def is_biblioteca_disponivel(self):
        return os.path.isfile(self.caminho_biblioteca)


    @property
    def nome_convencao_chamada(self):
        for convencao, nome in satcomum.constantes.CONVENCOES_CHAMADA:
            if convencao == self.convencao_chamada:
                return nome
        return u'(convencao desconhecida: {!r})'.format(self.convencao_chamada)


class Configuracoes(object):
    """

    Um arquivo de configurações de exemplo:

    .. sourcecode:: json

        {
            "debug": false,
            "usuario": "sathub",
            "senha": "sathub",
            "endpoints": [
                {
                    "alias": "900000001",
                    "descricao": "Tanca SDK-1000",
                    "codigo_ativacao": "12345678",
                    "caminho_biblioteca": "/opt/tanca/libsat64.so",
                    "convencao_chamada": 1
                },
                {
                    "alias": "900000002",
                    "descricao": "Dimep D-Sat",
                    "codigo_ativacao": "12345678",
                    "caminho_biblioteca": "/opt/dimep/libsatprotocol.so",
                    "convencao_chamada": 1
                },
                {
                    "alias": "900000003",
                    "descricao": "Bematech RB-1000 FI",
                    "codigo_ativacao": "123456789",
                    "caminho_biblioteca": "/opt/bematech/libbemasat64.so",
                    "convencao_chamada": 1
                },
            ]
        }

    """

    def __init__(self, origem=None):

        validator = Validator(schema={
                'debug': {
                        'type': 'boolean',
                        'required': True},
                'usuario': {
                        'type': 'string',
                        'required': True,
                        'minlength': 2,
                        'maxlength': 60},
                'senha': {
                        'type': 'string',
                        'required': True,
                        'minlength': 6},
                'endpoints': {
                        'type': 'list',
                        'required': True,
                        'minlength': 1,
                        'schema': {
                                'type': 'dict',
                                'schema': {
                                        'alias': {
                                                'type': 'string',
                                                'regex': r'^[a-zA-Z0-9-_]+$'},
                                        'descricao': {
                                                'type': 'string',
                                                'minlength': 1,
                                                'maxlength': 100},
                                        'codigo_ativacao': {
                                                'type': 'string',
                                                'required': True,
                                                'minlength': 1},
                                        'caminho_biblioteca': {
                                                'type': 'string',
                                                'required': True},
                                        'convencao_chamada': {
                                                'type': 'integer',
                                                'allowed': [v for v,s in satcomum.constantes.CONVENCOES_CHAMADA]}
                                    }
                            }
                    }
            }, purge_unknown=True)

        self._origem = origem or os.path.join(PROJECT_ROOT, 'config-sathub.json')

        if origem is None: # a origem do arquivo de configurações é a padrão
            if not os.path.isfile(self._origem):
                # arquivo de configurações padrão não existe;
                # cria um para que possa ser editado
                with open(self._origem, 'w') as f:
                    f.write(json.dumps(DEFAULT_CONFIG, indent=4))

        with open(self._origem, 'r') as f:
            self._confdata = json.load(f)

        validator.allow_unknown = True

        if not validator.validate(self._confdata):
            raise RuntimeError('Configuration error: {!r}'.format(
                    validator.errors))


    @property
    def origem(self):
        return self._origem


    @property
    def is_debug(self):
        return self._confdata['debug']


    @property
    def usuario(self):
        return self._confdata['usuario']


    @property
    def senha(self):
        return self._confdata['senha']


    @property
    def endpoints(self):
        return [Endpoint(**ep) for ep in self._confdata['endpoints']]


    def get_endpoint(self, alias):
        """Obtém os dados do ``Endpoint`` (*named tuple*) associado ao alias."""
        for ep in self._confdata['endpoints']:
            if ep['alias'] == alias:
                return Endpoint(**ep)
        raise ValueError('Endpoint nao encontrado, alias: {!r}'.format(alias))


    def descrever(self):
        """Descreve as configurações na saída padrão ou no terminal, se
        houver um.
        """
        import sathub
        _verbose(u'SATHub versão {}', sathub.__version__)

        for i, ep in enumerate(self.endpoints):
            _verbose('[-] Endpoint ({:d}) "{:s}"', i, ep.descricao)
            _verbose('[-]     Biblioteca "{:s}"', ep.caminho_biblioteca)
            _verbose('[-]     Convencao Chamada {:d} - {:s}',
                    ep.convencao_chamada, ep.nome_convencao_chamada)
            _verbose('[-] ')

        _verbose(u'')



def _configure_logging(config_path=None):
    filename = config_path or os.path.join(PROJECT_ROOT, 'config-log.json')

    if not os.path.isfile(filename):
        # arquivo de configurações de log não existe;
        # cria um para que possa ser editado se necessário
        with open(filename, 'w') as f:
            f.write(json.dumps(DEFAULT_LOGGING, indent=4))

    # carrega as configurações de logging e configura via dictConfig
    with open(filename, 'r') as f:
        logging_config = json.load(f)

    dictConfig(logging_config)


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


_configure_logging(config_path=os.environ.get('SATHUB_LOG_CONFIG_PATH'))

logger = logging.getLogger('sathub.conf')

conf = Configuracoes(origem=os.environ.get('SATHUB_CONFIG_PATH'))
