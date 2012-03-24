from modules.functions.helpers import *
from flask import Flask, flash, render_template, redirect, request
from modules.logging.logs import *
from db.db import *
from mongoengine import *
from modules.functions.context import *
from modules.users.models import *
from modules.notes.models import *
from modules.users.utils import *
from modules.pages.utils import *

@app.route("/settings")
def settings():
  from dropbox import client, rest, session
  from flask import session as flask_session

  flash('settings', 'btn')

  if(is_logged()):
    user = get_user()
    dropbox_session = user.get_dropbox_session()

    if(not dropbox_session):
      client = None

      sess = session.DropboxSession(dropbox_app_key(), dropbox_app_secret(), dropbox_access_type())
      request_token = sess.obtain_request_token()
      url = sess.build_authorize_url(request_token, oauth_callback=dropbox_callback_url())

      flask_session['session'] = sess
      flask_session['request_token'] = request_token
    else:
      client = client.DropboxClient(dropbox_session)
      url = None

    return render_template('users/settings.html', url=url, client=client)
  else:
    return redirect('/err_login')

@app.route("/settings/dropbox")
def settings_dropbox():
  from dropbox import client, rest, session
  from flask import session as flask_session
  import pickle

  if(is_logged()):
    try:
      sess = flask_session['session']
      request_token = flask_session['request_token']

      access_token = sess.obtain_access_token(request_token)

      user = get_user()
      user.dropbox_session = pickle.dumps(sess)
      user.save()

      flash('Your jabjot account has been linked to your Dropbox account.', 'notice')
      return redirect('/settings')
    except:
      flash('An error occurred and we couldn\'t link to your Dropbox account, please try again.', 'error')
      return redirect('/settings')
  else:
    return redirect('/err_login')

@app.route("/settings/unlink_dropbox")
def settings_unlink_dropbox():
  if(is_logged()):
    user = get_user()
    user.dropbox_session = None
    user.save()

    flash('Your Dropbox account has been unlinked.', 'notice')
    return redirect('/settings')
  else:
    return redirect('err_login')

@app.route("/settings/hide_dropbox_msg")
def settings_hide_dropbox_msg():
  if(is_logged()):
    user = get_user()
    user.hide_dropbox_msg = True
    user.save()

    flash('The message has been hidden.', 'notice')
    return redirect('/')
  else:
    return redirect('err_login')

@app.route("/settings/resync_dropbox")
def settings_resync_dropbox():
  if(is_logged()):
    user = get_user()
    if(user.dropbox_session):
      notes = Note.objects(user=user)

      for note in notes:
        note.synced = False
        note.save()

      flash('All your documents will be resynced.', 'notice')
    else:
      flash('Please first link your Dropbox account.', 'error')

    return redirect('/settings')
  else:
    return redirect('err_login')

@app.route("/settings/import_delicious", methods=['GET', 'POST'])
def settings_import_delicious():
  from BeautifulSoup import BeautifulSoup
  import datetime

  if(is_logged() and request.method == 'POST'):
    user = get_user()
    f = request.files['f']

    if(f and allowed_file_delicious(f.filename)):
      soup = BeautifulSoup(f.read())

      for item in soup.findAll(['dt']):
        i_title = None
        i_link = None
        private = False
        tags = None
        created_at = None
        content = ''

        if(item.nextSibling.name == 'dd'):
          content = item.nextSibling.contents[0]

        for link in item.findAll(['a']):
          if(link.has_key('href')):
            i_title = unicode(link.contents[0])
            i_link = link['href']

            if(link.has_key('private')):
              private = link['private']

              if(private == '0'):
                private = False
              else:
                private = True
            else:
              private = True

            if(link.has_key('tags')):
              tags = link['tags']
            else:
              tags = ''

            if(link.has_key('add_date')):
              created_at = datetime.datetime.fromtimestamp(int(link['add_date']))
            else:
              created_at = datetime.today()

        if(i_title and i_link and created_at):
          new_note = Note(user=user, title=i_title, content=content, kind='bookmark', private=private, done=False, url=i_link, tags=tags, created_at=created_at, updated_at=created_at, synced=False)
          new_note.save()
          new_note.save_tags()

      flash('Your bookmarks have been imported!', 'notice')
      return redirect('/notes')
    else:
      flash('That type of file is not allowed.', 'error')
      return redirect('/settings')
  else:
    flash('Something has gone wrong, please try again.', 'error')
    return redirect('/settings')

@app.route("/err_login")
def err_login():
  return render_template('users/err_login.html')

@app.route("/err_404")
def err_404():
  return render_template('users/err_404.html')

@app.route("/err_perms")
def err_perms():
  return render_template('users/err_perms.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
  flash('register', 'btn')
  if(not is_logged()):
    if(request.method == 'POST'):
      username = request.form['user[username]']
      email = request.form['user[email]']
      password = request.form['user[password]']
      active = 'yes'
      level = 'user'
      curr_user = {
        'email':email,
        'username':username,
        'password':password,
        'active':active,
        'level':level
      }

      if(email != '' and username != '' and password != '' and active != '' and level != ''):
        alr_user = User.objects(Q(email=email) | Q(username=username))

        if(not alr_user):
          new_user = User(email=email, username=username, password=md5(app.secret_key + ':' + password), active=active, level=level)
          new_user.save()

          flash('You have registered.  Please login:', 'notice')
          return redirect('/login')
        else:
          flash('User already exists, please select different username and/or email', 'error')
          return render_template('users/register.html', user=curr_user)
      else:
        flash('Please fill in all fields.', 'error')
        return render_template('users/register.html', user=curr_user)
    if(request.method == 'GET'):
      if(is_logged()):
        flash('You\'re already logged in!', 'error')
        return redirect('/')
      else:
        return render_template('users/register.html', user=None)
  else:
    flash("You've already registered and logged in.", "error")
    return redirect('/')

@app.route("/logout")
def logout():
  if(is_logged()):
    do_logout()
  flash('You have successfully logged out.', 'notice')
  return redirect('/')

@app.route("/login", methods=['GET', 'POST'])
def login():
  flash('login', 'btn')
  if(not is_logged()):
    if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']

      if(username != "" and password != ""):
        logged = do_login(username, password)

        if(logged):
          flash('You have logged in successfully.', 'notice')
          resp = do_login_cookie(logged)
          return resp
        else:
          flash('Wrong username or password.', 'error')
          return render_template('users/login.html')
      else:
        flash('Please enter your username and password.', 'error')
        return render_template('users/login.html')
    else:
      return render_template('users/login.html')
  else:
    flash("You've already logged in.", "error")
    return redirect('/')

@app.route("/users/init")
def init_users():
  if(is_admin()):
    """Initialize user for first time use, watch out, it deletes all users"""
    alr_user = User.objects(username='admin')

    if(not alr_user):
      new_user = User(email="admin@email.com", username='admin', password=md5(app.secret_key + ':' + 'admin'), active="yes", level="admin")
      new_user.save()

      return "Created user: admin"
    else:
      return "User already exists!"
  else:
    return redirect('/err_perms')

@app.route("/users/new", methods=['GET', 'POST'])
def users_new():
  method='new'
  if(is_admin()):
    if request.method == 'POST':
      email = request.form['user[email]']
      username = request.form['user[username]']
      password = request.form['user[password]']
      active = request.form['user[active]']
      level = request.form['user[level]']
      curr_user = {
        'email':email,
        'username':username,
        'password':password,
        'active':active,
        'level':level
      }

      if(email != '' and username != '' and password != '' and active != '' and level != ''):
        alr_user = User.objects(Q(email=email) | Q(username=username))

        if(not alr_user):
          new_user = User(email=email, username=username, password=md5(app.secret_key + ':' + password), active=active, level=level)
          new_user.save()

          flash('User has been created', 'notice')
          return redirect('/users')
        else:
          flash('User already exists, please select different username and/or email', 'error')
          return render_template('users/form.html', user=curr_user, method=method)
      else:
        flash('Please fill in all fields.', 'error')
        return render_template('users/form.html', user=curr_user, method=method)
    else:
      user = None
      return render_template('users/form.html', user=user, method=method)
  else:
    return redirect('/err_perms')

@app.route("/users/edit/<user_id>", methods=['GET', 'POST'])
def users_edit(user_id):
  method='edit'

  if(is_admin()):
    try:
      edit_user = User.objects(id=user_id)[0]
    except IndexError:
      flash('User not found', 'error')
      return redirect('/users')

    if(not edit_user):
      flash('User doesn\'t exist', 'error')
      return render_template('users/form.html', user=curr_user, method=method)
    else:
      if request.method == 'POST':
        email = request.form['user[email]']
        username = request.form['user[username]']
        password = request.form['user[password]']
        active = request.form['user[active]']
        level = request.form['user[level]']
        curr_user = {
          'id':user_id,
          'email':email,
          'username':username,
          'password':password,
          'active':active,
          'level':level
        }

        if(email != '' and username != '' and password != '' and active != '' and level != ''):
          edit_user.email = curr_user['email']
          edit_user.username = curr_user['username']
          edit_user.active = curr_user['active']
          edit_user.level = curr_user['level']

          if(curr_user['password'] != edit_user['password']):
            edit_user.password = md5(app.secret_key + ':' + curr_user['password'])

          edit_user.save()

          flash('User has been modified', 'notice')
          return redirect('/users/' + user_id)
        else:
          flash('Please fill in all fields.', 'error')
          return render_template('users/form.html', user=curr_user, method=method)
      else:
        return render_template('users/form.html', user=edit_user, method=method)
  else:
    return redirect('/err_perms')

@app.route("/users")
def users_index():
  if(is_admin()):
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
      users = User.objects(Q(username__contains=q) | Q(email__contains=q)).order_by('username')[start_index:end_index]
    else:
      users = User.objects.order_by('username')[start_index:end_index]

    return render_template('users/index.html', users=users, p=p, pagesize=get_page_size(), results=len(users), q=q)
  else:
    return redirect('/err_perms')

@app.route("/users/del/<user_id>")
def users_del(user_id):
  if(is_admin()):
    try:
      user = User.objects(id=user_id)[0]
    except IndexError:
      flash('User not found', 'error')
      return redirect('/users')

    if(user):
      user.delete()
      flash('User has been deleted', 'notice')
      return redirect('/users')
    else:
      flash('User doesn\'t exist', 'error')
      return redirect('/users')
  else:
    return redirect('/err_perms')

@app.route("/users/<user_id>")
def users_view(user_id):
  try:
    user = User.objects(id=user_id)[0]
  except IndexError:
    flash('User not found', 'error')
    return redirect('/users')
  else:
    if(is_admin()):
      notes = Note.objects(user=user)
    else:
      notes = None

  return render_template('users/view.html', user=user, notes=notes)

@app.route("/user/rss/private/<user_hash>")
def users_rss_private(user_hash):
  import datetime
  import PyRSS2Gen as RSS2

  parts = user_hash.split('_')

  if(len(parts) > 0):
    user_id = parts[0]
    rss_hash = parts[1]

    try:
      user = User.objects(id=user_id)[0]
    except IndexError:
      return 'Wrong hash!'
    else:
      # Check rss hash
      if(user.rss_hash() == rss_hash):
        notes = Note.objects(user=user).order_by('-created_at')[:20]
        notes_items = []

        for note in notes:
          notes_items.append(
            RSS2.RSSItem(
              title = note.title,
              link = note.get_url_rss(),
              description = note.get_dropbox_content(),
              guid = RSS2.Guid("http://jabjot.com/notes/" + str(note.id)),
              pubDate = note.created_at
            )
          )

        rss = RSS2.RSS2(
          title = user.username + "'s private notes feed - jabjot",
          link = "http://jabjot.com/user/rss/private/" + str(user.id) + '_' + user.rss_hash(),
          description = user.username + "'s latest notes.",
          lastBuildDate = datetime.datetime.utcnow(),
          items = notes_items
        )

        return rss.to_xml(encoding='utf-8')
      else:
        return 'Wrong hash!'
  else:
    return 'Wrong hash!'

@app.route("/user/rss/<user_id>")
def users_rss_public(user_id):
  import datetime
  import PyRSS2Gen as RSS2

  try:
    user = User.objects(id=user_id)[0]
  except IndexError:
    return 'Wrong user ID!'
  else:
    notes = Note.objects(user=user, private=False).order_by('-created_at')[:20]
    notes_items = []

    for note in notes:
      notes_items.append(
        RSS2.RSSItem(
          title = note.title,
          link = note.get_url_rss(),
          description = note.get_dropbox_content(),
          guid = RSS2.Guid("http://jabjot.com/notes/" + str(note.id)),
          pubDate = note.created_at
        )
      )

    rss = RSS2.RSS2(
      title = user.username + "'s public notes feed - jabjot",
      link = "http://jabjot.com/user/rss/" + str(user.id),
      description = user.username + "'s latest public notes.",
      lastBuildDate = datetime.datetime.utcnow(),
      items = notes_items
    )

    return rss.to_xml(encoding='utf-8')