from modules.functions.helpers import *
from flask import Flask, session, request, make_response, redirect
from db.db import *
from mongoengine import *
from modules.users.models import *

def delete_old_sessions(user):
  """Deletes old sessions for the user"""
  from datetime import datetime, timedelta
  date = datetime.today() - timedelta(days=120)
  
  old_sessions = Session.objects(user=user, created_at__lt=date)
  
  for os in old_sessions:
    os.delete()

def do_logout():
  """Logs out the user"""
  if(is_logged()):
    user = get_user()
    
    delete_old_sessions(user)
    
    alr_session = get_session()
    
    if(alr_session):
      alr_session.delete()
    
    session['user_session'] = None

def do_login_cookie(login_hash):
  """Saves session to cookie"""
  resp = make_response(redirect('/'))
  resp.set_cookie('user_session', login_hash, max_age=get_cookie_life())
  return resp

def do_login(username, password):
  from datetime import datetime, date
  
  """Logs in the user"""
  try:
    user = User.objects(username=username, password=md5(app.secret_key + ':' + password))[0]
    
    delete_old_sessions(user)
  
    today = date.today()
    key = '%(username)s:%(email)s:%(date)s' % {
      'username':user.username,
      'email':user.email,
      'date':today.strftime("%Y-%m-%d")
    }
    key_hashed = md5(key)
    new_session = Session(key=key_hashed, user=user, created_at=datetime.today())
    new_session.save()
    session['user_session'] = key_hashed
    return key_hashed
  except IndexError:
    pass

def get_session():
  """Gets current user's session"""
  try:
    s = session['user_session']
  except KeyError:
    s = request.cookies.get('user_session')
  
  if(s):
    db_session = Session.objects(key=s)
  
    if(db_session):
      return db_session[0]

def is_logged():
  s = get_session()
  
  if(s):
    return True

def get_user():
  s = get_session()
  
  if(s):
    return s.user

def is_admin():
  user = get_user()
  
  if(user):
    if(user.level == 'admin'):
      return True