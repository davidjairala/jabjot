from modules.functions.helpers import *
from mongoengine import *

class User(Document):
  email = StringField(max_length=255)
  username = StringField(required=True, max_length=255)
  password = StringField(required=True, max_length=255)
  active = StringField(required=True, max_length=50)
  level = StringField(required=True, max_length=50)
  dropbox_session = StringField(required=False)
  hide_dropbox_msg = BooleanField(required=False, default=False)
  
  def __unicode__(self):
    return self.username
  
  def get_dropbox_session(self):
    import pickle
    
    if(self.dropbox_session):
      return pickle.loads(str(self.dropbox_session))
  
  def rss_hash(self):
    return md5(self.email + '_' + self.username + '_' + self.password)

class Session(Document):
  key = StringField(required=True, max_length=255)
  user = ReferenceField(User)
  created_at = DateTimeField(required=True)
  
  def __unicode__(self):
    return self.user.username