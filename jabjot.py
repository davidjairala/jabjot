#!/usr/bin/python
from flask import Flask
app = Flask('jabjot')

from modules.functions.helpers import *

from db.db import *
from modules.users.models import *
from modules.users.controller import *
from modules.pages.controller import *
from modules.notes.controller import *
from modules.tags.controller import *
from modules.api.controller import *
from modules.images.controller import *

app.secret_key = 'jabjot_jo1hhzor'

if __name__ == "__main__":
  print('running: http://127.0.0.1:5000')
  app.run()