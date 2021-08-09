# Configuration of the system, need to be changed to run, especially for transcription


class Database(object):
    USER = 'Enter Your username Of database'
    PASSWORD = 'Enter Your Username of PWD'
    NAME = '123group9'


class XFYUN(object):
    """
    An account should be registered to generate the transcription
    """
    APPID = 'Register the APPID From XUNFEI'
    SecretKey = 'Register the SecretKey From XUNFEI'


class DefaultConfig(object):
    ENV = 'product'
    SECRET_KEY = 'f0293u0wef'


class AppRun(object):
    """
    parameters for the flask run
    """
    host = '127.0.0.1'
    port = 5000
    debug = False
