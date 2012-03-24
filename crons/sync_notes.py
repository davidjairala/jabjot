from mongoengine import Q
from modules.functions.helpers import *
from modules.users.models import *
from modules.notes.models import *
from dropbox import client
from dropbox.rest import ErrorResponse
from datetime import datetime, timedelta
from time import strptime, mktime

def sync_notes():
  count_notes = 0
  delta = timedelta(hours=6)

  users = User.objects(dropbox_session__ne=None)

  for user in users:
    print("=====================")
    print("Syncing: %s" % (user.username))

    # Check dropbox link
    user_client = client.DropboxClient(user.get_dropbox_session())

    # Check if we have access to folder, if not crash
    try:
      folder = user_client.metadata('/')

      # Check if we gotta delete notes from dropbox
      delete_notes = NoteDeleteDropbox.objects(user=user)

      for dnote in delete_notes:
        print("=====================")
        print("Deleting: %s" % (dnote.dropbox_name.encode('utf-8')))

        try:
          r = user_client.file_delete('/' + dnote.dropbox_name.encode('utf-8'))
        except:
          print("Couldn't delete!")

        dnote.delete()

      notes = Note.objects(Q(synced=False) | Q(synced__ne=True))

      for note in notes:
        print("=====================")
        try:
          print("Note: " + note.title)
        except UnicodeEncodeError:
          print("Note: " + note.title.encode('utf-8'))

        dbn = note.get_dropbox_name().encode('utf-8')
        content = note.get_dropbox_content().encode('utf-8')

        try:
          r = user_client.put_file('/' + dbn, content, overwrite=True)

          print(r)

          note.synced = True
          note.save()

          count_notes += 1

          if(count_notes >= 100):
            print("Done 100, break!")
            return 0
        except ErrorResponse:
          print("500 error when trying to save!")

      print("=====================")
      print("Downloads for: %s" % (user.username))

      for f in folder['contents']:
        if(not f['is_dir'] and f['mime_type'] == 'text/plain'):
          do_add = False

          try:
            file_name = f['path'].split('/')[1].replace('_-_', '/')
            parts = file_name.split('.')
            parts.remove('txt')
            file_name = '.'.join(parts)

            # Search for title
            try:
              alr_note = Note.objects(title=file_name)[0]

              # Note exists, lets compare dates
              dropbox_date = datetime.fromtimestamp(mktime(strptime(f['modified'], '%a, %d %b %Y %H:%M:%S +0000')))
              dropbox_date -= delta

              if(dropbox_date > alr_note.dropbox_updated_at):
                # Note on dropbox is newer, lets update
                alr_note.dropbox_updated_at = datetime.today()
                alr_note.content = user_client.get_file(f['path']).read().decode('utf-8')
                alr_note.synced = True
                alr_note.save()

                print("Updated from dropbox: %s" % (alr_note.title))
            except IndexError:
              do_add = True
          except IndexError:
            # Doesnt exist, lets download and add
            do_add = True
            file_name = f['path'].split('/')[1].split('.')[0].replace('_-_', '/').decode('utf-8')

          if(do_add):
            content = user_client.get_file(f['path']).read().decode('utf-8')
            new_note = Note(user=user, title=file_name, content=content, kind='note', private=True, done=False, created_at=datetime.today(), updated_at=datetime.today(), dropbox_updated_at=datetime.today(), synced=False, tags='')
            new_note.save()

            try:
              r = user_client.file_delete(f['path'].encode('utf-8'))
            except:
              print("Couldn't delete!")

            print("=====================")
            print("Note: " + new_note.title)

            count_notes += 1

            if(count_notes >= 100):
              print("Done 100, break!")
              return 0
    except ErrorResponse as (errno, strerror):
      send_email(msg='Exception error: %s' % (strerror), from_email='admin@yourdomain.com', to_email='admin@yourdomain.com', subject='jabjot dropbox sync error!')
      print("Link is dead!")
      user.dropbox_session = None
      user.hide_dropbox_msg = False
      user.save()
