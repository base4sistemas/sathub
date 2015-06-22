# -*- coding: utf-8 -*-
# runserver.py

from sathub import app
from sathub import sathubconf
app.run(host='0.0.0.0', debug=sathubconf.debug)
