import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "a-default-secret-key"

app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
