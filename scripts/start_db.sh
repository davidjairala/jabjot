#!/bin/bash
#mongod --dbpath /Applications/mongo/db/ &
#mongod --fork --logpath /var/www/jabjot/log/mongodb.log --logappend -f db/mongo_config.txt &
mongod -f db/mongo_config.txt &