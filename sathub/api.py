# -*- coding: utf-8 -*-
#
# sathub/api.py
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

from flask.ext import restful

from sathub import app

from sathub.resources.comunicarcertificadoicpbrasil import ComunicarCertificadoICPBRASIL
from sathub.resources.enviardadosvenda import EnviarDadosVenda
from sathub.resources.cancelarultimavenda import CancelarUltimaVenda
from sathub.resources.consultarsat import ConsultarSAT
from sathub.resources.testefimafim import TesteFimAFim
from sathub.resources.consultarstatusoperacional import ConsultarStatusOperacional
from sathub.resources.consultarnumerosessao import ConsultarNumeroSessao
from sathub.resources.configurarinterfacederede import ConfigurarInterfaceDeRede
from sathub.resources.associarassinatura import AssociarAssinatura
from sathub.resources.atualizarsoftwaresat import AtualizarSoftwareSAT
from sathub.resources.extrairlogs import ExtrairLogs
from sathub.resources.bloquearsat import BloquearSAT
from sathub.resources.desbloquearsat import DesbloquearSAT
from sathub.resources.trocarcodigodeativacao import TrocarCodigoDeAtivacao

api = restful.Api(app)

api.add_resource(ComunicarCertificadoICPBRASIL, '/hub/v1/comunicarcertificadoicpbrasil')
api.add_resource(EnviarDadosVenda, '/hub/v1/enviardadosvenda')
api.add_resource(CancelarUltimaVenda, '/hub/v1/cancelarultimavenda')
api.add_resource(ConsultarSAT, '/hub/v1/consultarsat')
api.add_resource(TesteFimAFim, '/hub/v1/testefimafim')
api.add_resource(ConsultarStatusOperacional, '/hub/v1/consultarstatusoperacional')
api.add_resource(ConsultarNumeroSessao, '/hub/v1/consultarnumerosessao')
api.add_resource(ConfigurarInterfaceDeRede, '/hub/v1/configurarinterfacederede')
api.add_resource(AssociarAssinatura, '/hub/v1/associarassinatura')
api.add_resource(AtualizarSoftwareSAT, '/hub/v1/atualizarsoftwaresat')
api.add_resource(ExtrairLogs, '/hub/v1/extrairlogs')
api.add_resource(BloquearSAT, '/hub/v1/bloquearsat')
api.add_resource(DesbloquearSAT, '/hub/v1/desbloquearsat')
api.add_resource(TrocarCodigoDeAtivacao, '/hub/v1/trocarcodigodeativacao')
