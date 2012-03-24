# JabJot
Bookmarking, note taking and todo-ing in Python/Flask/MongoDB

See it in action: [http://jabjot.com/](http://jabjot.com/)

# Features
* Keep your notes, bookmarks, and to-do's organized under the same open sourced web-app.
* You can fully control the application using keyboard shortcuts for speed and efficiency.
* Full notes, bookmarks and to-do's synchronization with your Dropbox account so you can access your notes on all your devices.
* Simple web scraping to keep an archive of all your bookmarks.
* RSS feeds.
* Email notes.
* And much more!

# Requirements
* flask
* mongoengine
* BeautifulSoup (for HTML scraping)
* dropbox (for [Dropbox integration](https://www.dropbox.com/developers) - also you'd need to register your app, get app key and secret)

# Installation
* Install all requirements.
* Clone the repo and create a MongoDB database for the application called 'jabjot' (you can change the name, just remember to change it on db/db.py as well).

Set up a username and password for the database and copy them to db/db.py:
    
    db_user = 'jabjot'
    db_password = 'mongo_db_password'
    db = connect('jabjot', username=db_user, password=db_password)
    
* Modify **modules/users/controller.py** function **init_users()** (*line 257*):

Change the line:
    
    if(is_admin()):

To:
    
    if(not is_admin()):
    
Just so it allows you to run this function just this one time.  Remember to change it back after running it.
* On a terminal, run ./jabjot.py (remember to chmod +x it).  Then point your browser to [http://127.0.0.1:5000/users/init](http://127.0.0.1:5000/users/init) to init the admin user.  You should see the following text:

    Created user: admin

* You should now be able to login at [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login).  Remember to change the admin user's password, email, etc. to your preferred settings.

# Other settings to change

Other things you might want to change eventually, all of them in **modules/functions/helpers.py**:

* **get_app_title()** to your app's title
* **get_app_url()** to your app's URL
* **get_app_email()** to your app's Email
* **dropbox_app_key()** **dropbox_app_secret()** if you set up your app with Dropbox and want Dropbox integration.

If you want to test sending mails on your local box but don't have a mail sender installed (we use Gmail in that case):

* **gmail_user()** and **gmail_pwd()** to your Gmail's accounts settings.

# Crons

Finally, there are two crons that need to be setup in order for the app to run to its fullest potential.  **sync_notes.py** syncs the users' notes with their Dropbox accounts if they chose to in their settings (I do just to have a backup and a way to edit notes, todos and bookmarks offline), and **scraper.py** which scrapes HTML off bookmarks very simply, just to have an archive available for the users.  They're both in the **crons** folder.  I have them set up to run every 5 minutes, and it works great but I leave that up to you.