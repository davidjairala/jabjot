from flask import Flask
app = Flask('jabjot')

import re
from jinja2 import Markup, escape
from modules.functions.helpers import *

@app.template_filter()
def nl2br(value):
  _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
  
  #result = u'\n\n'.join(u'%s<br />' % p.replace('\n', '<br>\n') for p in _paragraph_re.split(escape(value)))
  result = value.replace('\n', '<br />')
  result = Markup(result)
  return result

@app.template_filter()
def do_datetime(value):
  months = months_arr()
  month = months[value.month]
  s = value.strftime("%d/") + month + value.strftime("/%Y %H:%M")
  return s

@app.template_filter()
def urlencode(value):
  from urllib import quote_plus
  
  return quote_plus(value.encode('utf-8'))

@app.template_filter()
def markdown(value):
  import markdown

  return markdown.markdown(value)

@app.template_filter()
def count(l):
  return len(l)

@app.template_filter()
def get_rel_path(path):
  return get_rel_uploads_path(path)

@app.template_filter()
def get_tb(path):
  import os

  path = get_rel_uploads_path(path)
  f, ext = os.path.splitext(path)
  
  return "%s_300%s" % (f, ext)

@app.template_filter()
def get_tb_big(path):
  import os

  path = get_rel_uploads_path(path)
  f, ext = os.path.splitext(path)
  
  return "%s_500%s" % (f, ext)