from flask import abort, jsonify

from app.ext.database import db
from app.ext.database.models import *


def index_test():
    return 'hello world!'

