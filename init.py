from flask import Flask
from utilities.CONFIG import DefaultConfig


def create_app(name):
    app = Flask(name, static_url_path='')
    app.config.from_object(DefaultConfig)
    return app


if __name__== '__main__':
    from utilities.db import db_create
    db_create()
    print("Successfully create database.")