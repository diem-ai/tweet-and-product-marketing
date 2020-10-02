# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from dataviz.app.home import blueprint
from flask import render_template, redirect, url_for

from jinja2 import TemplateNotFound

@blueprint.route('/index')
# @login_required
def index():
    return render_template('index.html')

@blueprint.route('/<template>')
def route_template(template):
    try:
        return render_template(template + '.html')

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500
