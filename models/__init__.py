#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
import os

# Comment out for final project
# os.environ['HBNB_ENV'] = 'real'
# os.environ['HBNB_TYPE_STORAGE'] = 'db'
# os.environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
# os.environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
# os.environ['HBNB_MYSQL_HOST'] = 'localhost'
# os.environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'

storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
