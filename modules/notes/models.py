from mongoengine import *
from modules.functions.helpers import *
from modules.users.models import *

class Tag(Document):
  user = ReferenceField(User, required=True)
  name = StringField(required=True)

  def __unicode__(self):
    return self.user.username + ": " + self.name

  def to_json(self):
    return {'id': str(self.id), 'user_id': str(self.user.id), 'name': self.name, 'url': 'http://jabjot.com/notes?q=tag:' + self.name}

class Note(Document):
  user = ReferenceField(User, required=True)
  title = StringField(required=True)
  content = StringField()
  kind = StringField(required=True)
  private = BooleanField(required=True)
  done = BooleanField(required=True)
  url = StringField()
  tags = StringField()
  created_at = DateTimeField(required=True)
  updated_at = DateTimeField(required=True)
  dropbox_updated_at = DateTimeField(required=True)
  synced = BooleanField(required=False, default=False)
  scrape = StringField(required=False)

  def __unicode__(self):
    return self.user.username + ": " + self.title.encode('utf-8') + " (" + self.kind + ")"

  def get_url_rss(self):
    if(self.kind == 'bookmark' and self.url and self.url != ""):
      return self.url
    else:
      return "http://jabjot.com/notes/" + str(self.id)

  def to_json(self):
    return {'id': str(self.id), 'user_id': str(self.user.id), 'title': self.title, 'content': self.content, 'kind': self.kind, 'private': self.private, 'done': self.done, 'url': self.url, 'tags': self.tags, 'created_at': str(self.created_at), 'updated_at': str(self.updated_at), 'dropbox_updated_at': str(self.dropbox_updated_at), 'synced': self.synced}

  def get_email_text(self):
    txt = self.title + "\n" + get_app_url() + "notes/" + str(self.id) + "\n" + self.get_kind()

    if(self.kind == 'todo'):
      txt += "\nDone: " + self.get_done()

    if(self.tags and self.tags != ''):
      txt += "\nTags: " + self.tags

    if(self.url and self.url != ''):
      txt += "\n\nURL:\n" + self.url

    if(self.content and self.content != ''):
      txt += "\n\n" + txt_separator() + "\n" + \
      "CONTENT:" + \
      "\n" + txt_separator() + "\n\n" + \
       self.content

    if(self.scrape and self.scrape != ''):
      txt += "\n\n" + txt_separator() + "\n" + \
      "HTML SCRAPE:" + \
      "\n" + txt_separator() + "\n\n" + \
      self.scrape

    return txt.encode('utf-8')

  def get_dropbox_name(self):
    title = self.title.replace('/', '_-_').replace('\n', ' ')

    return title + '.txt'

  def get_dropbox_content(self):
    if(self.kind == 'bookmark'):
      if(not self.content or self.content == ''):
        return self.url
      else:
        try:
          self.content.index(self.url)
          return self.content
        except ValueError:
          return self.content + '\n\n' + self.url
    elif(self.kind == 'todo'):
      if(not self.content or self.content == ''):
        return self.get_done()
      else:
        try:
          self.content.index(self.get_done())
          return self.content
        except ValueError:
          return self.content + '\n\n' + self.get_done()
    else:
      return self.content

  def set_dropbox_delete(self):
    """Mark note for deletion at dropbox"""
    if(self.user.get_dropbox_session()):
      new_note_delete_dropbox = NoteDeleteDropbox(user=self.user, dropbox_name=self.get_dropbox_name())
      new_note_delete_dropbox.save()

  def is_owned(self, user):
    if(self.user == user):
      return True

  def get_kind(self):
    if(self.kind == 'note'):
      return 'Note'
    elif(self.kind == 'bookmark'):
      return 'Bookmark'
    elif(self.kind == 'todo'):
      return 'To-Do'

  def get_done(self):
    if(self.done):
      return 'Done'
    else:
      return 'Not yet done'

  def get_private(self):
    if(self.private):
      return 'Private'
    else:
      return 'Public'

  def link_tags(self):
    from urllib import quote_plus
    tags = self.split_tags()

    if(tags):
      out_tags = []

      for tag in tags:
        out_tags.append('<a href="/notes?q=tag:' + quote_plus(tag) + '">' + tag + '</a>')

      return ', '.join(out_tags)

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

class NoteDeleteDropbox(Document):
  user = ReferenceField(User, required=True)
  dropbox_name = StringField(required=True)

  def __unicode__(self):
    return self.user.username + ": " + self.dropbox_name
