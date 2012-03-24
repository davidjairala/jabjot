from flask import Flask, get_flashed_messages
app = Flask('jabjot')

from jinja2 import evalcontextfilter
from modules.functions.helpers import *
from modules.users.utils import *

@app.context_processor
def inject_context():
  messages = get_flashed_messages(["btn"])
  if(len(messages) > 0 and messages[0] and messages[0][1]):
    btn = messages[0][1]
  else:
    btn = ""

  context = {
    'is_logged':is_logged(),
    'is_admin':is_admin(),
    'user':get_user(),
    'app_version':get_app_version(),
    'app_url':get_app_url(),
    'app_title':get_app_title(),
    'btn':btn,
  }

  return dict(context=context)
