#!/usr/bin/python3
"""create a unique FileStorage instance for your application"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import getenv


storage_type = getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
