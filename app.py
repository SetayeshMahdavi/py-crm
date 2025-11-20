import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "a-default-secret-key"
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, 'crm.db')
    SQLALCHEMY_TRACK_MODIFICATIONS= False


app=Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)

class Customer:
    id=db.Column('')