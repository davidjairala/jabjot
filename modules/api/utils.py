from modules.functions.helpers import *
from db.db import *
from mongoengine import *
from modules.users.utils import *
from modules.api.models import *

def app_key(app):
  return md5(str(app.user.id) + ':' + str(app.id) + ':' + app.name + ':' + app.url)

def api_app(app_key):
  try:
    curr_app = App.objects(key=app_key)[0]
    
    return curr_app
  except IndexError:
    pass

def api_user(user, password):
  try:
    user = User.objects(username=user, password=md5(app.secret_key + ':' + password))[0]
    
    return user
  except IndexError:
    pass