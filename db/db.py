from mongoengine import *

db_user = 'jabjot'
db_password = 'db_password'
db = connect('jabjot', username=db_user, password=db_password)