# -*- coding: utf-8 -*-
#
# sathub/comum/util.py
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
import os
import random
import sys

from satcfe import DLLSAT
from satcfe import conf as satcfeconf
from satcfe import ClienteSATLocal
from satcfe.base import FuncoesSAT

from .config import conf


NUM_SESSAO_MIN = 100000
NUM_SESSAO_MAX = 999999

NUM_CAIXA_MIN = 0
NUM_CAIXA_MAX = 999

NUM_CAIXAS_MAX = (NUM_CAIXA_MAX - NUM_CAIXA_MIN) + 1

NUM_POR_FAIXA = int((NUM_SESSAO_MAX - NUM_SESSAO_MIN) / NUM_CAIXAS_MAX)


def faixa_numeracao(numero_caixa):
    """
    Retorna a faixa de numeração de sessão para o número do caixa.

    .. sourcecode:: python

        >>> a, b = faixa_numeracao(0) # caixa 0
        >>> NUM_SESSAO_MIN <= a <= NUM_SESSAO_MAX
        True
        >>> NUM_SESSAO_MIN <= b <= NUM_SESSAO_MAX
        True

        >>> x, y = faixa_numeracao(999) # caixa 999
        >>> NUM_SESSAO_MIN <= x <= NUM_SESSAO_MAX
        True
        >>> NUM_SESSAO_MIN <= y <= NUM_SESSAO_MAX
        True

    """
    _num_caixa = numero_caixa + 1
    n_min = ((_num_caixa * NUM_POR_FAIXA) + NUM_SESSAO_MIN) - NUM_POR_FAIXA
    n_max = (_num_caixa * NUM_POR_FAIXA) + NUM_SESSAO_MIN
    if _num_caixa > 1:
       n_min += 1
    return n_min, n_max


class NumeradorSessaoPorCaixa(object):
    """
    Um numerador de sessões persistente, gravando os números gerados em
    arquivos no formato JSON.

    Para evitar problemas de concorrência no acesso ao arquivo e para anular a
    possibilidade de números de sessão conflitantes entre os caixa, cada
    caixa terá o seu próprio arquivo de númeração de sessão e sua própria
    faixa de numeração, usando o seguinte esquema:

    A ER SAT deixa claro, no atributo B14 (``numeroCaixa``) que são possíveis
    caixas númerados entre 0 e 999, o que dá a possibilidade de 1000 caixas.

    Os números de sessão devem ser números de 6 dígitos, o que dá um limite
    entre 100000 e 999999. Assim, 999999-100000 dá 899999 que, se dividido
    por 1000 (caixas) dá uma faixa de cerca de 899:

    .. sourcecode:: python

        >>> 999999 - 100000
        899999
        >>> 899999 / 1000
        899

    Assim, cada caixa terá a sua própria faixa de numeração de sessão, o que
    torna impossível conflitos de número de sessão. Além disso, cada caixa
    terá um arquivo próprio, onde os números gerados serão persistidos,
    garantindo que os últimos 100 números gerados para aquele caixa não serão
    repetidos.

    +-------+-----------------------------+
    | Caixa | Faixa de Números de Sessão  |
    +=======+=============================+
    |   0   | 100000 a 100899             |
    +-------+-----------------------------+
    |   1   | 100900 a 101798             |
    +-------+-----------------------------+
    |                 ...                 |
    +-------+-----------------------------+
    |  999  | 998102 a 999000             |
    +-------+-----------------------------+

    """

    def __init__(self, tamanho=100, numero_caixa=1):
        super(NumeradorSessaoPorCaixa, self).__init__()
        self._memoria = []
        self._tamanho = tamanho
        self._numero_caixa = numero_caixa

        assert NUM_CAIXA_MIN <= self._numero_caixa <= NUM_CAIXA_MAX, \
                'Numero do caixa fora da faixa (0..999): {}'.format(
                        self._numero_caixa)

        self._arquivo_json = os.path.join(conf.pasta_projeto,
                'sessoes-cx-{}.json'.format(self._numero_caixa))


    def __call__(self, *args, **kwargs):
        while True:
            numero = random.randint(*faixa_numeracao(self._numero_caixa))
            if numero not in self._memoria:
                self._memoria.append(numero)
                if len(self._memoria) > self._tamanho:
                    self._memoria.pop(0) # remove o mais antigo
                break
        self._escrever_memoria()
        return numero


    def _carregar_memoria(self):
        self._memoria[:] = []
        if os.path.exists(self._arquivo_json):
            with open(self._arquivo_json, 'r') as f:
                self._memoria = json.load(f)

        assert isinstance(self._memoria, list), \
                "Memoria de numeracao de sessao deve ser um objeto 'list'; "\
                "obtido {}".format(type(self._memoria))


    def _escrever_memoria(self):
        with open(self._arquivo_json, 'w') as f:
            json.dump(self._memoria, f)


def memoize(fn):
    # Implementação de memoize obtida de "Thumbtack Engineering"
    # https://www.thumbtack.com/engineering/a-primer-on-python-decorators/
    stored_results = {}

    def memoized(*args):
        try:
            # try to get the cached result
            return stored_results[args]
        except KeyError:
            # nothing was cached for those args. let's fix that.
            result = stored_results[args] = fn(*args)
            return result

    return memoized


@memoize
def instanciar_numerador_sessao(numero_caixa):
    return NumeradorSessaoPorCaixa(numero_caixa=numero_caixa)


@memoize
def instanciar_funcoes_sat(numero_caixa):
    funcoes_sat = FuncoesSAT(
            dll=DLLSAT(
                    caminho=conf.caminho_dll,
                    convencao=conf.convencao_chamada),
            numerador_sessao=instanciar_numerador_sessao(numero_caixa))
    return funcoes_sat


@memoize
def instanciar_cliente_local(numero_caixa):
    cliente = ClienteSATLocal(
            dll=DLLSAT(caminho=conf.caminho_dll,
                    convencao=conf.convencao_chamada),
            numerador_sessao=instanciar_numerador_sessao(numero_caixa))
    return cliente


def hexdump(data):
    def _cut(sequence, size):
        for i in xrange(0, len(sequence), size):
            yield sequence[i:i+size]
    _hex = lambda seq: ['{0:02x}'.format(b) for b in seq]
    _chr = lambda seq: [chr(b) if 32 <= b <= 126 else '.' for b in seq]
    raw_data = map(ord, data)
    hexpanel = [' '.join(line) for line in _cut(_hex(raw_data), 16)]
    chrpanel = [''.join(line) for line in _cut(_chr(raw_data), 16)]
    hexpanel[-1] = hexpanel[-1] + (chr(32) * (47 - len(hexpanel[-1])))
    chrpanel[-1] = chrpanel[-1] + (chr(32) * (16 - len(chrpanel[-1])))
    return '\n'.join('%s  %s' % (h, c) for h, c in zip(hexpanel, chrpanel))
