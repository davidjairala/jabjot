from modules.functions.helpers import *
from flask import Flask, flash, render_template, redirect, request
from modules.logging.logs import *
from db.db import *
from mongoengine import *
from modules.functions.filters import *
from modules.users.utils import *
from modules.pages.utils import *
from modules.notes.models import *

@app.route("/err_private")
def err_private():
  flash('notes', 'btn')
  return render_template('notes/err_private.html')

@app.route("/notes/resync/<id>")
def notes_resync(id):
  flash('notes', 'btn')
  if(is_logged()):
    try:
      user = get_user()
      note = Note.objects(id=id)[0]

      if(note.is_owned(user)):
        note.synced = False
        note.save()

        flash('Note marked for resync', 'notice')
        return redirect('/notes/' + id)
      else:
        return redirect('/err_perms')
    except IndexError:
      flash('Note not found', 'error')
      return redirect('/notes')
  else:
    return redirect('/err_login')

@app.route("/notes/new", methods=['GET', 'POST'])
def notes_new():
  from datetime import datetime
  date = datetime.today()
  method='new'
  flash('notes', 'btn')

  bookmark = request.args.get('bookmark')
  todo = request.args.get('todo')
  bookmarklet = request.args.get('bookmarklet')

  if(bookmarklet):
    # Check if note already exists
    if(request.args.get('url')):
      try:
        alr_bookmark = Note.objects(url=request.args.get('url'))[0]
        return redirect('/notes/edit/' + str(alr_bookmark.id) + '?bookmarklet=1')
      except IndexError:
        pass
    bookmarklet = True
    kind = 'bookmark'
  else:
    bookmarklet = False
    if(bookmark == "1"):
      kind = 'bookmark'
    elif(todo == "1"):
      kind = 'todo'
    else:
      kind = 'note'

  if(is_logged()):
    if request.method == 'POST':
      try:
        if(request.form['bookmarklet']):
          bookmarklet = True
      except:
        bookmarklet = False

      user = get_user()
      title = request.form['note[title]']
      content = request.form['note[content]']
      kind = request.form['note[kind]']

      if(request.form['note[private]'] == "private"):
        private = True
      else:
        private = False

      url = request.form['note[url]']

      if(request.form['note[done]'] == "yes"):
        done = True
      else:
        done = False

      tags = request.form['note[tags]']

      if(not tags or tags.strip() == 'None'):
        tags = ''

      created_at = date
      updated_at = date
      dropbox_updated_at = date
      curr_note = {
       'user': user,
       'title': title,
       'content': content,
       'kind': kind,
       'private': private,
       'done': done,
       'tags': tags,
       'url': url,
       'created_at': created_at,
       'updated_at': updated_at,
       'dropbox_updated_at': dropbox_updated_at,
      }

      if(user != '' and title != '' and kind != '' and private != '' and done != '' and created_at != '' and updated_at != '' and dropbox_updated_at != ''):
        alr_note = Note.objects(user=user, title=title)

        if(not alr_note):
          new_note = Note(user=user, title=title, content=content, kind=kind, private=private, done=done, tags=tags, url=url, created_at=created_at, updated_at=updated_at, dropbox_updated_at=dropbox_updated_at, synced=False)
          new_note.save()
          new_note.save_tags()

          if(bookmarklet):
            return render_template('notes/done_save.html')
          else:
            flash('Note has been created', 'notice')
            return redirect('/notes')
        else:
          flash('Note already exists.', 'error')
          return render_template('notes/form.html', note=curr_note, method=method, bookmarklet=bookmarklet)
      else:
        flash('Please fill in all fields.', 'error')
        return render_template('notes/form.html', note=curr_note, method=method, bookmarklet=bookmarklet)
    else:
      if(request.args.get('title')):
        title = request.args.get('title')
      else:
        title = ''

      if(request.args.get('url')):
        url = request.args.get('url')
      else:
        url = ''

      return render_template('notes/form.html', note={'private':True, 'kind':kind, 'url':url, 'title':title}, method=method, bookmarklet=bookmarklet)
  else:
    return redirect('/err_login')

@app.route("/notes/edit/<id>", methods=['GET', 'POST'])
def notes_edit(id):
  from datetime import datetime
  date = datetime.today()
  method='edit'
  bookmarklet = False
  flash('notes', 'btn')

  if(request.args.get('bookmarklet')):
    bookmarklet = True
  else:
    try:
      if(request.method == 'POST' and request.form['bookmarklet']):
        bookmarklet = True
    except:
      pass

  if(is_logged()):
    try:
      user = get_user()
      edit_note = Note.objects(id=id)[0]

      if(edit_note.is_owned(user)):
        if(not edit_note.url):
          edit_note.url = ''

        if(not edit_note.tags or edit_note.tags.strip() == 'None'):
          edit_note.tags = ''

        if request.method == 'POST':
          title = request.form['note[title]']
          content = request.form['note[content]']
          kind = request.form['note[kind]']

          if(request.form['note[private]'] == "private"):
            private = True
          else:
            private = False

          url = request.form['note[url]']

          if(request.form['note[done]'] == "yes"):
            done = True
          else:
            done = False

          tags = request.form['note[tags]']

          if(not tags or tags.strip() == 'None'):
            tags = ''

          updated_at = date
          dropbox_updated_at = date
          curr_note = {
            'id': edit_note.id,
            'title': title,
            'content': content,
            'kind': kind,
            'private': private,
            'done': done,
            'tags': tags,
            'url': url,
            'updated_at': date,
            'dropbox_updated_at':dropbox_updated_at,
          }

          if(title != '' and kind != '' and private != '' and done != ''):
            # Mark for dropbox deletion
            edit_note.set_dropbox_delete()

            edit_note.title = curr_note['title']
            edit_note.content = curr_note['content']
            edit_note.kind = curr_note['kind']
            edit_note.private = curr_note['private']
            edit_note.done = curr_note['done']
            edit_note.tags = curr_note['tags']
            edit_note.url = curr_note['url']
            edit_note.updated_at = curr_note['updated_at']
            edit_note.dropbox_updated_at = curr_note['dropbox_updated_at']
            edit_note.synced = False

            edit_note.save()
            edit_note.save_tags()

            if(bookmarklet):
              return render_template('notes/done_save.html')
            else:
              flash('Note has been modified', 'notice')
              return redirect('/notes/' + id)
          else:
            flash('Please fill in all fields.', 'error')
            return render_template('notes/form.html', note=curr_note, method=method,
                bookmarklet=bookmarklet)
        else:
          return render_template('notes/form.html', note=edit_note, method=method,
              bookmarklet=bookmarklet)
      else:
        return redirect('/err_perms')
    except IndexError:
      flash('Note not found', 'error')
      return redirect('/notes')
  else:
    return redirect('/err_login')

@app.route("/notes")
def notes_index():
  flash('notes', 'btn')

  if(is_logged()):
    user = get_user()
    q = request.args.get('q')

    if(not q):
      q = ''

    p = request.args.get('p')

    try:
      p = int(p)
    except (ValueError, TypeError):
      p = 1

    if(p <= 0):
      p = 1

    start_index = (p - 1) * get_page_size()
    end_index = p * get_page_size()

    if(q):
      try:
        q.index('title:')
        q_temp = q.replace('title:', '').strip()
        query = searchify(q_temp)

        notes = Note.objects(title=query, user=user).order_by('-updated_at')[start_index:end_index]
      except ValueError:
        try:
          q.index('tag:')
          q_temp = q.replace('tag:', '').strip()
          query = searchify(q_temp)

          notes = Note.objects(tags=query, user=user).order_by('-updated_at')[start_index:end_index]
        except ValueError:
          try:
            q.index('content:')
            q_temp = q.replace('content:', '').strip()
            query = searchify(q_temp)

            notes = Note.objects(content=query, user=user).order_by('-updated_at')[start_index:end_index]
          except ValueError:
            try:
              q.index('url:')
              q_temp = q.replace('url:', '').strip()
              query = searchify(q_temp)

              notes = Note.objects(url=query, user=user).order_by('-updated_at')[start_index:end_index]
            except ValueError:
              try:
                q.index('kind:')
                q_temp = q.replace('kind:', '').strip()
                query = searchify(q_temp)

                notes = Note.objects(kind=query, user=user).order_by('-updated_at')[start_index:end_index]
              except ValueError:
                query = searchify(q)

                notes = Note.objects((Q(title=query) | Q(content=query) | Q(url=query) | Q(tags=query)), user=user).order_by('-updated_at')[start_index:end_index]
    else:
      notes = Note.objects(user=user).order_by('-updated_at')[start_index:end_index]

    return render_template('notes/index.html', notes=notes, p=p, pagesize=1, results=len(notes), q=q)
  else:
    return redirect('/err_login')

@app.route("/notes/del/<id>")
def notes_del(id):
  from dropbox import client
  flash('notes', 'btn')

  if(is_logged()):
    try:
      user = get_user()
      note = Note.objects(id=id)[0]

      if(note.is_owned(user)):
        note.set_dropbox_delete()

        note.delete()
        flash('Note has been deleted', 'notice')

        # Check where to redirect
        url_cookie = request.cookies.get(app_name() + '_last_url')

        if(url_cookie and url_cookie != ""):
          return redirect(url_cookie)
        else:
          return redirect('/notes')
      else:
        return redirect('/err_perms')
    except IndexError:
      flash('Note not found', 'error')
      return redirect('/notes')
  else:
    return redirect('/err_login')

@app.route("/notes/<id>")
def notes_view(id):
  flash('notes', 'btn')

  try:
    user = get_user()
    note = Note.objects(id=id)[0]

    if(not note.private or (is_logged() and note.is_owned(user))):
      try:
        next_note = Note.objects(updated_at__lt=note.updated_at).order_by('-updated_at')[0]
      except IndexError:
        next_note = None

      try:
        prev_note = Note.objects(updated_at__gt=note.updated_at).order_by('updated_at')[0]
      except IndexError:
        prev_note = None

      return render_template('notes/view.html', note=note, next_note=next_note, prev_note=prev_note)
    elif(note.private and not is_logged()):
      return redirect('/err_private')
    elif(is_logged() and not note.is_owned(user)):
      return redirect('/err_private')
  except (IndexError, ValidationError):
    flash('Note not found', 'error')
    return redirect('/notes')

@app.route("/notes/ac", methods=["GET"])
def ac():
  if(is_logged()):
    q = request.args.get('q').strip()

    if(q and q != ''):
      tags = Tag.objects(user=get_user(), name__istartswith=q).order_by('name')[:5]

      return render_template('notes/ac.html', tags=tags)
    else:
      return 'err_q'
  else:
    return 'err_login'

@app.route("/tools")
def tools():
  flash('tools', 'btn')
  return render_template('notes/tools.html')

@app.route("/notes/toggle_done")
def toggle_done():
  if(is_logged()):
    id = request.args.get('id')
    done = request.args.get('done')

    if(done == "1"):
      done = True
    else:
      done = False

    try:
      user = get_user()
      note = Note.objects(id=id)[0]

      if(note.is_owned(user)):
        note.done = done
        note.save()

        return 'ok'
      else:
        return 'err_owner'
    except IndexError:
      return 'err_not_found'
  else:
    return 'err_logged'

@app.route("/notes/email/<id>", methods=["GET", "POST"])
def notes_email(id):
  flash('notes', 'btn')

  try:
    note = Note.objects(id=id)[0]
    user = get_user()

    if(not note.private or (is_logged() and note.is_owned(user))):
      if(request.method == 'POST'):
        email = request.form['email']

        if(email and email != ''):
          send_email(msg=note.get_email_text(), from_email=get_app_email(), to_email=user.email, subject=note.title + ' - ' + get_app_title())

          flash('The note has been sent.', 'notice')
          return redirect('/notes/' + id)
        else:
          flash('Please fill in an email address', 'error')

      return render_template('notes/email.html', note=note)
    elif(note.private and not is_logged()):
      return redirect('/err_private')
    elif(is_logged() and not note.is_owned(user)):
      return redirect('/err_private')
  except (IndexError, ValidationError):
    flash('Note not found', 'error')
    return redirect('/notes')

@app.route("/notes/get_scrape/<id>", methods=["GET"])
def get_scrape(id):
  if(is_logged()):
    try:
      user = get_user()
      note = Note.objects(id=id)[0]

      if(note.is_owned(user)):
        return render_template('notes/get_scrape.html', note=note)
      else:
        return 'err_owner'
    except IndexError:
      return 'err_not_found'
  else:
    return 'err_login'
