from modules.users.utils import *

def get_admin_view(name, fields):
  html = """{% extends "base.html" %}

{% block title %}
  View """ + name.capitalize() + """ -
{% endblock %}

{% block content %}
  <div class="page-header">
    <h1>
      <a href="/""" + name + """s">""" + name.capitalize() + """</a> -
      View
    </h1>
  </div>"""

  for field in fields:
    html += """
  <p>
    <strong>""" + field.capitalize() + """:</strong>
    <br />
    {{ """ + name + """.""" + field + """ }}
  </p>"""

  html += """
  {% if context.is_admin %}
    <p>
      <a href="/""" + name + """s">back</a>
      <a href="/""" + name + """s/edit/{{ """ + name + """.id }}">edit</a>
      <a href="/""" + name + """s/del/{{ """ + name + """.id }}" onclick="return confirm('sure?');">del</a>
    </p>
  {% endif %}
{% endblock %}"""

  return html

def get_admin_index(name, fields):
  html = """{% extends "base.html" %}

{% block title %}
  """ + name.capitalize() + """s -
{% endblock %}

{% block content %}
  <div class="page-header">
    <h1>
      <a href="/""" + name + """s">""" + name.capitalize() + """s</a>
    </h1>
  </div>

  <form method="get" action="/""" + name + """s">
    <p>
      <input type="text" name="q" value="{{ q }}" />
      <input type="submit" value="Search" />
    </p>
  </form>

  <table>
    <thead>
      <tr>"""

  for field in fields:
    html += """
        <th>""" + field + """</th>"""

  html += """
        <th colspan="3">
          <!-- i -->
        </th>
      </tr>
    </thead>
    <tbody>
      {% for """ + name + """ in """ + name + """s %}
        <tr>"""

  for field in fields:
    html += """
          <td>{{""" + name + """.""" + field + """}}</td>"""

  html += """
          <td>
            <a href="/""" + name + """s/{{ """ + name + """.id }}">view</a>
          </td>
          <td>
            <a href="/""" + name + """s/edit/{{ """ + name + """.id }}">edit</a>
          </td>
          <td>
            <a href="/""" + name + """s/del/{{ """ + name + """.id }}" onclick="return confirm('sure?');">del</a>
          </td>
        </tr>
      {% endfor %}
    </tbody>
  </table>

  {% if p > 1 or results >= pagesize %}
    <div class="pagination">
      <ul>
        {% if p > 1 %}
          <li>
            <a href="/""" + name + """s?p={{ p - 1}}&q={{ q }}">&larr; Previous</a>
          </li>
        {% endif %}
        {% if results >= pagesize %}
          <li>
            <a href="/""" + name + """s?p={{ p + 1}}&q={{ q }}">Next &rarr;</a>
          </li>
        {% endif %}
      </ul>
    </div>
  {% endif %}

  <br />
  <p>
    <a href="/""" + name + """s/new">new_""" + name + """</a>
  </p>
{% endblock %}"""

  return html

def get_admin_form(name, fields):
  html = """{% extends "base.html" %}

{% block title %}
  {{ title }} """ + name.capitalize() + """ -
{% endblock %}

{% block content %}
  <div class="page-header">
    <h1>
      <a href="/""" + name + """s">""" + name.capitalize() + """s</a> -
      {{ title }}
    </h1>
  </div>

  {% if method == "edit" %}
    <form method="post" action="/""" + name + """s/{{ method }}/{{ """ + name + """.id }}">
  {% else %}
    <form method="post" action="/""" + name + """s/{{ method }}">
  {% endif %}"""

  for field in fields:
    html += "\n\
    <p>\n\
      " + field.capitalize() + ":<br />\n\
      <input type=\"text\" name=\"" + name + "[" + field + "]\" value=\"{{ " + name + "." + field + " }}\" />\n\
    </p>\n"

  html += "\n\
    <p>\n\
      {% if method == \"edit\" %}\n\
        <input type=\"hidden\" name=\"" + name + "_id\" value=\"{{ " + name + ".id }}\" />\n\
        <input type=\"submit\" value=\"Edit\" class=\"bold\" />\n\
      {% else %}\n\
        <input type=\"submit\" value=\"Create\" class=\"bold\" />\n\
      {% endif %}\n\
    </p>\n\
  </form>\n\
{% endblock %}"""

  return html

def get_admin_model(name, fields):
  html = """from mongoengine import *

class """ + name.capitalize() + """(Document):\n"""

  for field in fields:
    html += "  " + field + " = StringField(required=True, max_length=255)\n"

  html += """
  def __unicode__(self):
    return self.""" + fields[0]

  return html

def get_admin_controller(name, fields):
  html = """from modules.functions.helpers import *
from flask import Flask, flash, render_template, redirect, request
from modules.logging.logs import *
from db.db import *
from mongoengine import *
from modules.functions.filters import *
from modules.users.utils import *
from modules.pages.utils import *
from modules.""" + name + """s.models import *

@app.route("/""" + name + """s/new", methods=['GET', 'POST'])
def """ + name + """s_new():
  method = 'new'
  title = 'New'
  if(is_admin()):
    if request.method == 'POST':\n"""

  for field in fields:
    html += """      """ + field + """ = request.form['""" + name + """[""" + field + """]']\n"""

  html += """      curr_""" + name + """ = {\n"""

  for field in fields:
    html += """       '""" + field + """': """ + field + """,\n"""

  html += """      }

      if("""
  html += ' != \'\' and '.join(fields) + ' != \'\'):'

  html += """
        alr_""" + name + """ = """ + name.capitalize() + """.objects(""" + fields[0] + """=""" + fields[0] + """)

        if(not alr_""" + name + """):
          new_""" + name + """ = """ + name.capitalize() + """("""

  for field in fields:
    html += field + "=" + field + ","

  html = html[:-1]

  html += """)
          new_""" + name + """.save()

          flash('""" + name.capitalize() + """ has been created', 'notice')
          return redirect('/""" + name + """s')
        else:
          flash('""" + name.capitalize() + """ already exists.', 'error')
          return render_template('""" + name + """s/form.html', """ + name + """=curr_""" + name + """, method=method)
      else:
        flash('Please fill in all fields.', 'error')
        return render_template('""" + name + """s/form.html', """ + name + """=curr_""" + name + """, method=method)
    else:
      return render_template('""" + name + """s/form.html', """ + name + """=None, method=method)
  else:
    return redirect('/err_perms')

@app.route("/""" + name + """s/edit/<id>", methods=['GET', 'POST'])
def """ + name + """s_edit(id):
  method = 'edit'
  title = 'Edit'
  if(is_admin()):
    try:
      edit_""" + name + """ = """ + name.capitalize() + """.objects(id=id)[0]
    except IndexError:
      flash('""" + name.capitalize() + """ not found', 'error')
      return redirect('/""" + name + """s')

    if request.method == 'POST':\n"""

  for field in fields:
    html += """      """ + field + """ = request.form['""" + name + """[""" + field + """]']\n"""

  html += """      curr_""" + name + """ = {\n"""
  html += """        'id': edit_""" + name + """.id,\n"""

  for field in fields:
    html += """        '""" + field + """': """ + field + """,\n"""

  html += """      }

      if("""
  html += ' != \'\' and '.join(fields) + ' != \'\'):\n'

  for field in fields:
    html += """        edit_""" + name + """.""" + field + """ = curr_""" + name + """['""" + field + """']\n"""

  html += """
        edit_""" + name + """.save()

        flash('""" + name.capitalize() + """ has been modified', 'notice')
        return redirect('/""" + name + """s/' + id)
      else:
        flash('Please fill in all fields.', 'error')
        return render_template('""" + name + """s/form.html', """ + name + """=curr_""" + name + """, method=method)
    else:
      return render_template('""" + name + """s/form.html', """ + name + """=edit_""" + name + """, method=method)
  else:
    return redirect('/err_perms')

@app.route("/""" + name + """s")
def """ + name + """s_index():
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
      """ + name + """s = """ + name.capitalize() + """.objects(""" + fields[0] + """__icontains=q)[start_index:end_index]
    else:
      """ + name + """s = """ + name.capitalize() + """.objects[start_index:end_index]
    return render_template('""" + name + """s/index.html', """ + name + """s=""" + name + """s, p=p, pagesize=get_page_size(), results=len(""" + name + """s), q=q)
  else:
    return redirect('/err_perms')

@app.route("/""" + name + """s/del/<id>")
def """ + name + """s_del(id):
  if(is_admin()):
    try:
      """ + name + """ = """ + name.capitalize() + """.objects(id=id)[0]
    except IndexError:
      flash('""" + name.capitalize() + """ not found', 'error')
      return redirect('/""" + name + """s')

    """ + name + """.delete()
    flash('""" + name.capitalize() + """ has been deleted', 'notice')
    return redirect('/""" + name + """s')
  else:
    return redirect('/err_perms')

@app.route("/""" + name + """s/<id>")
def """ + name + """s_view(id):
  if(is_admin()):
    try:
      """ + name + """ = """ + name.capitalize() + """.objects(id=id)[0]

      return render_template('""" + name + """s/view.html', """ + name + """=""" + name + """)
    except IndexError:
      flash('""" + name.capitalize() + """ not found', 'error')
      return redirect('/""" + name + """s')
  else:
    return redirect('/err_perms')"""
  return html