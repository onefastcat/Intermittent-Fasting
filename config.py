import os

class Config(object):
    GREETING = 'Salutations, superior students!'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-key-for-devs'
