from flask import Flask
app = Flask('jabjot')

from modules.functions.helpers import *
from flask import render_template, redirect, request, flash
from modules.logging.logs import *
from mongoengine import *
from modules.functions.context import *
from modules.pages.utils import *
from modules.users.utils import *

@app.route("/admin")
def admin():
  flash('admin', 'btn')
  if(is_admin()):
    return render_template('pages/admin.html')
  else:
    return redirect('/err_perms')

@app.route("/generate_admins", methods=['GET', 'POST'])
def generate_admins():
  flash('admin', 'btn')
  if(is_admin()):
    if(request.method == 'POST'):
      name = request.form['name']
      fields = request.form['fields']
      fields = fields.split(',')
      f_fields = []

      for field in fields:
        if(field.strip() != ''):
          f_fields.append(field.strip())

      if(name != '' and len(f_fields) > 0):
        controller_html = get_admin_controller(name, f_fields)
        models_html = get_admin_model(name, f_fields)
        form_html = get_admin_form(name, f_fields)
        index_html = get_admin_index(name, f_fields)
        view_html = get_admin_view(name, f_fields)

        return render_template(
          'pages/do_generate_admins.html',
          name=name,
          controller_html=controller_html,
          models_html=models_html,
          form_html=form_html,
          index_html=index_html,
          view_html=view_html)
      else:
        flash('Please fill all fields', 'error')
        return render_template('pages/generate_admins.html', name=name, fields=','.join(fields))
    else:
      return render_template('pages/generate_admins.html')
  else:
    return redirect('/err_perms')

@app.route("/")
def frontpage():
  if(is_logged()):
    flash('notes', 'btn')
    return redirect('/notes')
  else:
    flash('frontpage', 'btn')
    return render_template('pages/frontpage.html')
