import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dwbvismrogb28db3p1ndjdfh'
