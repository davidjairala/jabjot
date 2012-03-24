#!/usr/bin/python
import sys
from db.db import *
from mongoengine import *
from crons.sync_notes import *
from crons.scraper import *

def main():
  arg = 'sync_notes'
  
  if(len(sys.argv) > 1):
    if(sys.argv[1] == 'sync_notes'):
      arg = 'sync_notes'
    elif(sys.argv[1] == 'scrape'):
      arg = 'scrape'
  
  if(arg == 'sync_notes'):
    sync_notes()
  elif(arg == 'scrape'):
    scrape()

if __name__ == "__main__":
  main()