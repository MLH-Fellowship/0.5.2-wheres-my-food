from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import Form
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)
# app.config.from_object('db/database')
# db = SQLAlchemy(app)
# Migrate(app,db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')




