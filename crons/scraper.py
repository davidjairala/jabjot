from mongoengine import Q
from modules.users.models import User
from modules.notes.models import Note
from modules.functions.html2text import *
from modules.functions.helpers import *
from modules.functions.timeout import *
from BeautifulSoup import BeautifulSoup
import urllib2

def scrape():
  try:
    notes = Note.objects(kind='bookmark', scrape=None).order_by('-updated_at')[0:20]
  
    for note in notes:
      set_timeout(20)
      skip = False
      
      if(note.url and note.url != ''):
        try:
          print(note.title)
        except UnicodeEncodeError:
          print(note.title.encode('utf-8'))
        print("")
        
        if(not is_mime(note.url, 'image') and not is_mime(note.url, 'pdf')):
          try:
            html = urllib2.urlopen(note.url).read()
            try:
              soup = BeautifulSoup(html)
            except UnicodeEncodeError:
              try:
                soup = BeautifulSoup(html.encode('utf-8'))
              except UnicodeDecodeError:
                try:
                  soup = BeautifulSoup(html.decode('utf-8'))
                except UnicodeDecodeError:
                  skip = True
          
            if(not skip):
              # Remove images
              [s.extract() for s in soup('img')]
    
              try:
                text = html2text(soup.prettify())
              except UnicodeDecodeError:
                try:
                  text = html2text(soup.prettify().decode('utf-8'))
                except HTMLParser.HTMLParseError:
                  text = ' '
              except (HTMLParser.HTMLParseError, ValueError):
                text = ' '
            else:
              text = ' '
              print("Invalid encoding or something not scrapable!")
      
            note.scrape = text
            note.save()
          except urllib2.HTTPError:
            note.scrape = ' '
            note.save()
            print("404 probably...")
          except urllib2.URLError:
            note.scrape = ' '
            note.save()
            print("temp url error...")
          except TimeoutException:
            note.scrape = ' '
            note.save()
            print("Timeout!")
        else:
          note.scrape = ' '
          note.save()
          print("URL is not HTML text")
      else:
        print("No URL!")
      print("==================")
  except IndexError:
      print("No more notes...")
