from modules.functions.helpers import *
from flask import Flask, flash, render_template, redirect, request
from modules.logging.logs import *
from db.db import *
from mongoengine import *
from modules.functions.filters import *
from modules.users.utils import *
from modules.pages.utils import *
from modules.images.models import *

@app.route("/images/new", methods=['GET', 'POST'])
def images_new():
  from datetime import datetime
  date = datetime.today()
  method='new'
  flash('images', 'btn')

  if(is_logged()):
    if request.method == 'POST':
      user = get_user()

      # Check if we gotta upload
      file_image = request.files['file_image']

      if(file_image and allowed_file_image(file_image.filename)):
        path = upload_file(file_image, get_uploads_path() + 'images/' + str(user.id))

        make_thumbnails(path, 500)
        tags = request.form['image[tags]']

        if(not tags or tags.strip() == 'None'):
          tags = ''

        curr_image = {
         'user': user,
         'path': path,
         'tags': tags,
         'created_at': date,
         'updated_at': date,
        }

        new_image = Image(user=user,path=path,tags=tags,created_at=date,updated_at=date)
        new_image.save()
        new_image.save_tags()

        flash('Image has been created', 'notice')
        return redirect('/images')
      elif(file_image and not allowed_file_image(file_image.filename)):
        flash('The image was not in one of the allowed formats: PNG, GIF OR JPG.', 'error')
        return render_template('images/form.html', image=curr_image, method=method)
      else:
        flash('Please fill in all fields.', 'error')
        return render_template('images/form.html', image=curr_image, method=method)
    else:
      return render_template('images/form.html', image=None, method=method)
  else:
    return redirect('/err_login')

@app.route("/images/edit/<id>", methods=['GET', 'POST'])
def images_edit(id):
  from datetime import datetime
  date = datetime.today()
  method='edit'
  flash('images', 'btn')

  if(is_logged()):
    try:
      edit_image = Image.objects(id=id)[0]
    except IndexError:
      flash('Image not found', 'error')
      return redirect('/images')

    if request.method == 'POST':
      user = get_user()
      tags = request.form['image[tags]']
      path = None

      curr_image = {
        'id': edit_image.id,
        'tags': tags,
      }

      # Check if we gotta upload
      file_image = request.files['file_image']

      if(file_image and allowed_file_image(file_image.filename)):
        path = upload_file(file_image, get_uploads_path() + 'images/' + str(user.id))

        make_thumbnails(path, 500)

        # Delete old image
        delete_thumbnails(edit_image.path, 500)
        delete_file(edit_image.path)
      elif(file_image and not allowed_file_image(file_image.filename)):
        flash('The image was not in one of the allowed formats: PNG, GIF OR JPG.', 'error')
        return render_template('images/form.html', image=curr_image, method=method)

      if(not tags or tags.strip() == 'None'):
        tags = ''

      if(path):
        edit_image.path = path

      edit_image.tags = curr_image['tags']
      edit_image.updated_at = date

      edit_image.save()
      edit_image.save_tags()

      flash('Image has been modified', 'notice')
      return redirect('/images/' + id)
    else:
      return render_template('images/form.html', image=edit_image, method=method)
  else:
    return redirect('/err_login')

@app.route("/images")
def images_index():
  flash('images', 'btn')

  if(is_logged()):
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
      images = Image.objects(tags__icontains=q)[start_index:end_index]
    else:
      images = Image.objects[start_index:end_index]
    return render_template('images/index.html', images=images, p=p, pagesize=get_page_size(), results=len(images), q=q)
  else:
    return redirect('/err_login')

@app.route("/images/del/<id>")
def images_del(id):
  flash('images', 'btn')

  if(is_logged()):
    try:
      image = Image.objects(id=id)[0]
    except IndexError:
      flash('Image not found', 'error')
      return redirect('/images')

    delete_thumbnails(image.path, 500)
    delete_file(image.path)
    image.delete()
    flash('Image has been deleted', 'notice')
    return redirect('/images')
  else:
    return redirect('/err_login')

@app.route("/images/<id>")
def images_view(id):
  flash('images', 'btn')

  if(is_logged()):
    try:
      image = Image.objects(id=id)[0]

      return render_template('images/view.html', image=image)
    except IndexError:
      flash('Image not found', 'error')
      return redirect('/images')
  else:
    return redirect('/err_login')