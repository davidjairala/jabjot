from modules.functions.helpers import *
from flask import Flask, flash, render_template, redirect, request
from modules.logging.logs import *
from db.db import *
from mongoengine import *
from modules.functions.filters import *
from modules.users.utils import *
from modules.notes.models import *
from modules.api.models import *
from modules.api.utils import *

@app.route("/api")
def api_index():
  return render_template('api/index.html')

@app.route("/api/apps")
def api_apps():
  if(is_logged()):
    user = get_user()
    apps = App.objects(user=user).order_by('name')
    
    return render_template('api/apps.html', apps=apps)
  else:
    return redirect('/err_login')

@app.route("/api/apps/edit/<id>", methods=['GET', 'POST'])
def api_apps_edit(id):
  if(is_logged()):
    try:
      user = get_user()
      curr_app = App.objects(id=id)[0]
      
      if(curr_app.is_owned(user)):
        app_name = curr_app.name
        app_url = curr_app.url
    
        if request.method == 'POST':
          app_name = request.form['app_name']
          app_url = request.form['app_url']
      
          if(app_name != '' and app_url != ''):
            curr_app.name = app_name
            curr_app.url = app_url
            
            if(not curr_app.key or curr_app.key == ''):
              curr_app.key = app_key(curr_app)
            
            curr_app.save()
        
            flash('The app has been saved successfully', 'notice')
            return redirect('/api/apps')
          else:
            flash('Please fill in all the fields.', 'error')
    
        return render_template('api/register.html', app_name=app_name, app_url=app_url, app_id=id, edit=True)
      else:
        flash("You can't edit that app.", 'error')
        return redirect('/api/apps')
    except IndexError:
      flash("Couldn't find that app, please try again.", 'error')
      return redirect('/api/apps')
  else:
    return redirect('/err_login')

@app.route("/api/apps/del/<id>")
def api_apps_del(id):
  if(is_logged()):
    try:
      user = get_user()
      curr_app = App.objects(id=id)[0]

      if(curr_app.is_owned(user)):
        curr_app.delete()
        flash("The app has been deleted.", "notice")
        return redirect('/api/apps')
      else:
        flash("You can't delete that app.", 'error')
        return redirect('/api/apps')
    except IndexError:
      flash("Couldn't find that app, please try again.", 'error')
      return redirect('/api/apps')
  else:
    return redirect('/err_login')

@app.route("/api/register", methods=['GET', 'POST'])
def api_register():
  if(is_logged()):
    user = get_user()
    app_name = ''
    app_url = ''
    
    if request.method == 'POST':
      app_name = request.form['app_name']
      app_url = request.form['app_url']
      
      if(app_name != '' and app_url != ''):
        alr_app = App.objects(Q(user=user) & (Q(name=app_name) | Q(url=app_url)))
        
        if(alr_app):
          flash('The app already exists!', 'error')
        else:
          new_app = App(user=user, name=app_name, url=app_url)
          new_app.key = app_key(new_app)
          new_app.save()
          
          flash('The app has been created successfully', 'notice')
          return redirect('/api/apps')
      else:
        flash('Please fill in all the fields.', 'error')
    
    return render_template('api/register.html', app_name=app_name, app_url=app_url, edit=False)
  else:
    return redirect('/err_login')

@app.route("/api/notes")
def api_notes():
  import json
  
  try:
    user = request.args.get('user').strip()
    password = request.args.get('password').strip()
    app_key = request.args.get('app_key').strip()
    try:
      start_index = request.args.get('start_index').strip()
    except AttributeError:
      start_index = 0
  
    curr_app = api_app(app_key)
  
    if(curr_app):
      user = api_user(user, password)
    
      if(user):
        if(start_index and start_index != '' and is_numeric(start_index)):
          start_index = int(start_index)
        else:
          start_index = 0
      
        end_index = start_index + 20
      
        notes = Note.objects(user=user).order_by('-created_at')[start_index:end_index]
        notes_arr = []
        
        for note in notes:
          notes_arr.append(note.to_json())
        
        return json.dumps(notes_arr)
      else:
        return 'error_user_not_found'
    else:
      return 'error_app_not_found'
  except AttributeError:
    return 'error_no_params'

@app.route("/api/notes/new", methods=['GET', 'POST'])
def api_notes_new():
  import json
  import re
  import json
  from datetime import datetime
  date = datetime.today()
  
  if request.method == 'POST':
    if(request.form.has_key('user') and request.form.has_key('password') and request.form.has_key('app_key') and request.form.has_key('title') and request.form.has_key('kind') and request.form.has_key('user') and request.form.has_key('private')):
      try:
        user = request.form['user'].strip()
        password = request.form['password'].strip()
        app_key = request.form['app_key'].strip()

        curr_app = api_app(app_key)

        if(curr_app):
          user = api_user(user, password)

          if(user):
            title = request.form['title'].strip()
            
            if(request.form.has_key('content')):
              content = request.form['content'].strip()
            else:
              content = ''
            
            kind = request.form['kind'].strip()
            private = request.form['private'].strip()
            
            if(request.form.has_key('done')):
              done = request.form['done'].strip()
            else:
              done = ''
            
            if(request.form.has_key('url')):
              url = request.form['url'].strip()
            else:
              url = ''
            
            if(request.form.has_key('tags')):
              tags = request.form['tags'].strip()
            else:
              tags = ''
          
            if(done == ''):
              done = "0"
          
            if(title != '' and kind != '' and private != ''):
              if(kind == 'note' or kind == 'bookmark' or kind == 'todo'):
                if(done == "1"):
                  done = True
                else:
                  done = False
              
                if(private == "1"):
                  private = True
                else:
                  private = False
              
                # Fix content
                content = content.replace('\\n', chr(10))
              
                new_note = Note(user=user, title=title, content=content, kind=kind, private=private, done=done, url=url, tags=tags, created_at=date, updated_at=date, dropbox_updated_at=date, synced=False)
                new_note.save()
                new_note.save_tags()
              
                return json.dumps(new_note.to_json())
              else:
                return 'error_wrong_kind'
            else:
              return 'error_no_params'
          else:
            return 'error_user_not_found'
        else:
          return 'error_app_not_found'
      except AttributeError:
        return 'error_no_params'
    else:
      return 'error_no_params'
  else:
    if(is_logged() and is_admin()):
      return render_template('api/new_note.html')
    else:
      return 'error_no_post'

@app.route("/api/notes/edit", methods=['GET', 'POST'])
def api_notes_edit():
  import json
  from datetime import datetime
  date = datetime.today()

  import json

  if request.method == 'POST':
    if(request.form.has_key('user') and request.form.has_key('password') and request.form.has_key('app_key') and request.form.has_key('id') and request.form.has_key('title') and request.form.has_key('kind') and request.form.has_key('user') and request.form.has_key('private')):
      try:
        user = request.form['user'].strip()
        password = request.form['password'].strip()
        app_key = request.form['app_key'].strip()

        curr_app = api_app(app_key)

        if(curr_app):
          user = api_user(user, password)

          if(user):
            id = request.form['id'].strip()
        
            try:
              note = Note.objects(id=id, user=user)[0]
            except IndexError:
              return 'error_note_not_found'
            else:
              title = request.form['title'].strip()
              
              if(request.form.has_key('content')):
                content = request.form['content'].strip()
              else:
                content = ''
              
              kind = request.form['kind'].strip()
              private = request.form['private'].strip()
              
              if(request.form.has_key('done')):
                done = request.form['done'].strip()
              else:
                done = ''
              
              if(request.form.has_key('url')):
                url = request.form['url'].strip()
              else:
                url = ''
              
              if(request.form.has_key('tags')):
                tags = request.form['tags'].strip()
              else:
                tags = ''

              if(done == ''):
                done = "0"

              if(title != '' and kind != '' and private != ''):
                if(kind == 'note' or kind == 'bookmark' or kind == 'todo'):
                  if(done == "1"):
                    done = True
                  else:
                    done = False

                  if(private == "1"):
                    private = True
                  else:
                    private = False
              
                  # Fix content
                  content = content.replace('\\n', chr(10))

                  note.title = title
                  note.content = content
                  note.kind = kind
                  note.private = private
                  note.done = done
                  note.url = url
                  note.tags = tags
                  note.updated_at = date
                  note.synced = False
                  note.set_dropbox_delete()
                  note.save()
                  note.save_tags()

                  return json.dumps(note.to_json())
                else:
                  return 'error_wrong_kind'
              else:
                return 'error_no_params'
          else:
            return 'error_user_not_found'
        else:
          return 'error_app_not_found'
      except AttributeError:
        return 'error_no_params'
    else:
      return 'error_no_params'
  else:
    if(is_logged() and is_admin()):
      return render_template('api/edit_note.html')
    else:
      return 'error_no_post'

@app.route("/api/notes/del", methods=['GET', 'POST'])
def api_notes_del():
  if request.method == 'POST':
    if(request.form.has_key('user') and request.form.has_key('password') and request.form.has_key('app_key') and request.form.has_key('id')):
      user = request.form['user'].strip()
      password = request.form['password'].strip()
      app_key = request.form['app_key'].strip()

      curr_app = api_app(app_key)
      
      if(curr_app):
        user = api_user(user, password)

        if(user):
          id = request.form['id'].strip()
          
          try:
            note = Note.objects(id=id, user=user)[0]
          except IndexError:
            return 'error_note_not_found'
          else:
            note.set_dropbox_delete()
            note.delete()
            
            return 'ok'
        else:
          return 'error_user_not_found'
      else:
        return 'error_app_not_found'
    else:
      return 'error_no_params'
  else:
    if(is_logged() and is_admin()):
      return render_template('api/del_note.html')
    else:
      return 'error_no_post'

@app.route("/api/tags")
def api_tags():
  import json

  try:
    user = request.args.get('user').strip()
    password = request.args.get('password').strip()
    app_key = request.args.get('app_key').strip()
    try:
      start_index = request.args.get('start_index').strip()
    except AttributeError:
      start_index = 0

    curr_app = api_app(app_key)

    if(curr_app):
      user = api_user(user, password)

      if(user):
        if(start_index and start_index != '' and is_numeric(start_index)):
          start_index = int(start_index)
        else:
          start_index = 0

        end_index = start_index + 20

        tags = Tag.objects(user=user).order_by('-created_at')[start_index:end_index]
        tags_arr = []

        for tag in tags:
          tags_arr.append(tag.to_json())

        return json.dumps(tags_arr)
      else:
        return 'error_user_not_found'
    else:
      return 'error_app_not_found'
  except AttributeError:
    return 'error_no_params'

@app.route("/api/tags_ac")
def api_tags_ac():
  import json

  try:
    user = request.args.get('user').strip()
    password = request.args.get('password').strip()
    app_key = request.args.get('app_key').strip()
    query = request.args.get('query').strip()

    curr_app = api_app(app_key)

    if(curr_app):
      user = api_user(user, password)

      if(user):
        if(query and query != ''):
          tags = Tag.objects(user=user, name__icontains=query).order_by('name')[:5]
          tags_arr = []

          for tag in tags:
            tags_arr.append(tag.to_json())

          return json.dumps(tags_arr)
        else:
          return 'error_empty_query'
      else:
        return 'error_user_not_found'
    else:
      return 'error_app_not_found'
  except AttributeError:
    return 'error_no_params'