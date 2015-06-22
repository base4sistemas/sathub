# -*- coding: utf-8 -*-
# sathub.wsgi

import os
import sys

localdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, localdir)

from sathub import app as application
