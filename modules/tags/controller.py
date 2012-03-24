from modules.functions.helpers import *
from flask import Flask, flash, render_template, redirect, request
from modules.logging.logs import *
from db.db import *
from mongoengine import *
from modules.functions.filters import *
from modules.users.utils import *
from modules.pages.utils import *
from modules.notes.models import *

@app.route("/tags/new", methods=['GET', 'POST'])
def tags_new():
  flash('tags', 'btn')
  method='new'
  if(is_logged()):
    if request.method == 'POST':
      user = get_user()
      name = request.form['tag[name]']
      curr_tag = {
       'user': user,
       'name': name,
      }

      if(user != '' and name != ''):
        alr_tag = Tag.objects(user=user)

        if(not alr_tag):
          new_tag = Tag(user=user,name=name)
          new_tag.save()

          flash('Tag has been created', 'notice')
          return redirect('/tags')
        else:
          flash('Tag already exists.', 'error')
          return render_template('tags/form.html', tag=curr_tag, method=method)
      else:
        flash('Please fill in all fields.', 'error')
        return render_template('tags/form.html', tag=curr_tag, method=method)
    else:
      return render_template('tags/form.html', tag=None, method=method)
  else:
    return redirect('/err_login')

@app.route("/tags/edit/<id>", methods=['GET', 'POST'])
def tags_edit(id):
  flash('tags', 'btn')
  method='edit'
  if(is_logged()):
    try:
      edit_tag = Tag.objects(id=id)[0]
    except IndexError:
      flash('Tag not found', 'error')
      return redirect('/tags')

    if request.method == 'POST':
      user = get_user()
      name = request.form['tag[name]']
      curr_tag = {
        'id': edit_tag.id,
        'user': user,
        'name': name,
      }

      if(user != '' and name != ''):
        edit_tag.user = curr_tag['user']
        edit_tag.name = curr_tag['name']

        edit_tag.save()

        flash('Tag has been modified', 'notice')
        return redirect('/tags')
      else:
        flash('Please fill in all fields.', 'error')
        return render_template('tags/form.html', tag=curr_tag, method=method)
    else:
      return render_template('tags/form.html', tag=edit_tag, method=method)
  else:
    return redirect('/err_login')

@app.route("/tags")
def tags_index():
  flash('tags', 'btn')
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
      tags = Tag.objects(user=user, name__icontains=q).order_by('name')[start_index:end_index]
    else:
      tags = Tag.objects(user=user).order_by('name')[start_index:end_index]
    return render_template('tags/index.html', tags=tags, p=p, pagesize=get_page_size(), results=len(tags), q=q)
  else:
    return redirect('/err_login')

@app.route("/tags/del/<id>")
def tags_del(id):
  flash('tags', 'btn')
  if(is_logged()):
    try:
      tag = Tag.objects(id=id)[0]
    except IndexError:
      flash('Tag not found', 'error')
      return redirect('/tags')

    tag.delete()
    flash('Tag has been deleted', 'notice')
    return redirect('/tags')
  else:
    return redirect('/err_login')