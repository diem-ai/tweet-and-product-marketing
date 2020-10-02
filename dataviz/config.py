# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   os import environ

class Config(object):

    basedir    = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = 'key'

    # THEME SUPPORT
    #  if set then url_for('static', filename='', theme='')
    #  will add the theme name to the static URL:
    #    /static/<DEFAULT_THEME>/filename
    # DEFAULT_THEME = "themes/dark"
    DEFAULT_THEME = None


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
