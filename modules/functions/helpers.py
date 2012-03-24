# -*- coding: utf-8 -*-

# Globals
from flask import Flask
app = Flask('jabjot')

def app_name():
  return 'jabjot'

def get_app_version():
  return "4"

def get_app():
  global app
  return app

def get_app_title():
  return 'jabjot'

def get_app_url():
  return 'http://jabjot.com/'

def get_app_email():
  return 'appemail@yourdomain.com'

def gmail_user():
  return 'gmailemail@gmail.com'

def gmail_pwd():
  return 'gmailpwd'

def get_page_size():
  return 20

def get_cookie_life():
  return 60*60*24*30

def get_app_path():
  import os

  path = os.path.realpath(__file__).split('/')
  path = '/'.join(path[0:len(path)-3]) + '/'

  return path

def get_uploads_path():
  path = get_app_path() + 'static/uploads/'

  return path

def get_rel_uploads_path(path):
  org_path = path
  path = path.split('/%s/' % (get_app_title()))
  if(len(path) > 0):
    path = '/' + path[1]
    return path
  else:
    return org_path

def get_just_path(path):
  org_path = path
  path = path.split('/')

  if(len(path) > 0):
    path = path[0:len(path) - 1]
    return '/'.join(path)
  else:
    return org_path

def txt_separator():
  return "============================"

def dropbox_app_key():
  return 'dropbox_app_key'

def dropbox_app_secret():
  return 'dropbox_app_secret'

def dropbox_access_type():
  return 'app_folder'

def dropbox_callback_url():
  return get_app_url() + 'settings/dropbox'

def months_arr():
  return ['', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

def md5(txt):
  import hashlib

  return hashlib.md5(txt).hexdigest()

def get_guid(name = None):
  import hashlib
  from datetime import datetime
  import random

  today = datetime.today()
  random.seed(today)
  key = '%(rand)s:%(date)s' % {
    'rand':str(random.randint(1,1000000)),
    'date':today.strftime("%Y-%m-%d %H:%I:%S")
  }

  h = hashlib.md5(key).hexdigest()

  if(name and name != ""):
    guid = h[0:5] + "_" + name
  else:
    guid = h[0:15]

  return guid

def slugify(s):
  import re

  s = quita_tildes(s)
  s = remove_extra_spaces(s)
  s = remove_quotes(s)
  s = strip_tabs(s)
  s = strip_tags(s)
  s = s.lower()
  s = s.strip()

  s = re.sub(' +', '_', s)
  s = re.sub('\'', '', s)
  s = re.sub('@', '_', s)
  s = re.sub('&', '_', s)
  s = re.sub('/\s*[^A-Za-z0-9\.\-]\s*/', '_', s)
  s = re.sub('_+', '_', s)
  s = re.sub('/\A[_\.]+|[_\.]+\z/', '', s)

  return s

def quita_tildes(txt):
  txt = txt.encode('utf-8')

  txt = txt.replace("Á", "A")
  txt = txt.replace("É", "E")
  txt = txt.replace("Í", "I")
  txt = txt.replace("Ó", "O")
  txt = txt.replace("Ú", "U")
  txt = txt.replace("Ñ", "N")
  txt = txt.replace("Ü", "U")

  txt = txt.replace("á", "a")
  txt = txt.replace("é", "e")
  txt = txt.replace("í", "i")
  txt = txt.replace("ó", "o")
  txt = txt.replace("ú", "u")
  txt = txt.replace("ñ", "n")
  txt = txt.replace("ü", "u")

  return txt

def remove_extra_spaces(txt):
  import re

  p = re.compile(' +')
  txt = p.sub(' ', txt).strip()

  return txt

def remove_quotes(txt):
  txt = txt.replace('"', '')
  txt = txt.replace("'", '')
  return txt

def strip_tabs(txt):
  import re

  p = re.compile(r'\t')
  txt = p.sub(' ', txt)
  p = re.compile(r' +')
  txt = p.sub(' ', txt)
  txt = txt.strip()

  return txt

def strip_tags(txt):
  import re

  p = re.compile(r'<[^>]*>')
  txt = p.sub(' ', txt)
  p = re.compile(r'\&nbsp;')
  txt = p.sub(' ', txt)

  return txt

def send_email(msg, from_email, to_email, subject):
  import smtplib
  from email.mime.text import MIMEText

  msg = MIMEText(msg)
  msg['Subject'] = subject
  msg['From'] = from_email
  msg['To'] = to_email

  try:
    # Production
    s = smtplib.SMTP('localhost')
  except:
    # Testing
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(gmail_user(), gmail_pwd())

  s.sendmail(from_email, [to_email], msg.as_string())
  s.quit()

def allowed_extensions_delicious():
  return ['html', 'htm']

def allowed_file_delicious(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions_delicious()

def allowed_extensions_image():
  return ['png', 'jpg', 'jpeg', 'gif']

def allowed_file_image(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions_image()

def searchify(txt):
  import re

  query = re.compile('((?=.*' + remove_extra_spaces(txt).replace(' ', '.*)(?=.*') + '.*))', re.IGNORECASE)

  return query

def search(q, token):
  from mongoengine import Q
  import re

  searchables = []
  q = re.sub(r'( )+', ' ', q).strip()
  q = re.sub(r'tag:', 'tags:', q)
  parts = q.split(' ')
  results = []

  for part in parts:
    try:
      if(part.index(token + ':') != None):
        try:
          tag = part.split(token + ':')[1].strip()
        except IndexError:
          pass
        finally:
          tag_parts = tag.split(',')

          if(len(tag_parts) > 1):
            for subtag in tag_parts:
              results.append(subtag.strip())
          else:
            results.append(tag)
    except ValueError:
      try:
        if(part.index(':') != None):
          pass
      except ValueError:
        pass

  if(len(results) > 0):
    return searchify(' '.join(results))
  else:
    return re.compile(r'')

def is_numeric(num):
  try:
    i = float(num)
  except ValueError, TypeError:
    return False
  else:
    return True

def is_mime(url, mime_type):
  """Returns true if the URL string is mime type mime_type"""
  import mimetypes

  mime = mimetypes.guess_type(url)

  if(len(mime) > 0):
    mime = mime[0]

    if(mime):
      try:
        return mime.lower().index(mime_type) != None
      except ValueError:
        return False

def guid():
  import uuid

  return str(uuid.uuid1())

def upload_file(file, path):
  import os

  f, ext = os.path.splitext(file.filename)
  mkdir(path)
  new_filename = guid() + ext
  new_path = os.path.join(path, new_filename)
  file.save(new_path)

  return new_path

def make_thumbnails(path, size):
  from PIL import Image
  import glob, os

  while(size > 0):
    f, ext = os.path.splitext(path)
    im = Image.open(path)
    im.thumbnail((size, size), Image.ANTIALIAS)
    im.save(f + "_%d%s" % (size, ext), "JPEG")
    size -= 50

def mkdir(path):
  import os

  try:
    os.mkdir(path)
  except OSError:
    pass

def delete_thumbnails(path, size):
  import os
  f, ext = os.path.splitext(path)

  while(size > 0):
    thumb_filename = "%s_%d%s" % (f, size, ext)
    delete_file(thumb_filename)
    size -= 50

def delete_file(path):
  import os

  try:
    os.remove(path)
  except OSError:
    pass