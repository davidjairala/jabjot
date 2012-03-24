from mongoengine import *
from modules.users.models import *
from modules.functions.helpers import *

class App(Document):
  user = ReferenceField(User, required=True)
  name = StringField(required=True)
  url = StringField(required=True)
  key = StringField(required=True)
  
  def __unicode__(self):
    return self.user.username + ': ' + self.name + ' : ' + self.url
  
  def is_owned(self, user):
    if(self.user == user):
      return True