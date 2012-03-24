from mongoengine import *
from modules.users.models import *
from modules.notes.models import Tag

class Image(Document):
  user = ReferenceField(User, required=True)
  path = StringField(required=True, max_length=255)
  tags = StringField()
  created_at = DateTimeField(required=True)
  updated_at = DateTimeField(required=True)

  def __unicode__(self):
    return "%s : %s" % (self.user.username, self.path)

  def split_tags(self):
    import re
    
    if(self.tags and self.tags.strip() != ''):
      tags = self.tags.strip()
      tags = re.sub(r',+', ',', tags).strip()
      tags = re.sub(r' +', ' ', tags).strip()
      tags = tags.split(',')
      
      return tags

  def save_tags(self):
    import re
    tags = self.split_tags()
    
    if(tags):
      out_tags = []
      
      for tag in tags:
        tag = tag.strip()
        
        if(tag != ''):
          try:
            out_tags.index(tag)
          except ValueError:
            out_tags.append(tag)
          
          alr_tag = Tag.objects(user=self.user, name=tag)
          
          if(not alr_tag):
            new_tag = Tag(user=self.user, name=tag)
            new_tag.save()
      
      self.tags = ','.join(out_tags)
      self.save()

  def get_url(self, size=None):
    import os

    head, tail = os.path.split(self.path)

    url = "%sstatic/uploads/images/%s/%s" % (get_app_url(), str(self.user.id), tail)

    if(not size):
      return url
    else:
      f, ext = os.path.splitext(url)
      url = "%s_%d%s" % (f, size, ext)
      return url

  def is_owned(self, user):
    if(self.user == user):
      return True