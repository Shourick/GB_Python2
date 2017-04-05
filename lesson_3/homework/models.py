import os
import sqlite3
import json
import datetime
from peewee import *

BASE_DIR = os.path.dirname(__file__)
DB_FILE_NAME = os.path.join(BASE_DIR, 'db.sqlite3')
DATA_BASE = SqliteDatabase(DB_FILE_NAME)

class MyModel(Model):
    class Meta:
        database = DATA_BASE


class Terminal(MyModel):
    configuration = JSO

class Payment(MyModel):
    date_time = DateTimeField(default=datetime.datetime.now())
    terminal = ForeignKeyField(Terminal, related_name='payment')

