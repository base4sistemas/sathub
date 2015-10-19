# -*- coding: utf-8 -*-
# runserver.py

from sathub import app
from sathub import conf
app.run(host='0.0.0.0', debug=conf.is_debug)
