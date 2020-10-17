from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import *
import core

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/")
def index():
	return ''


if __name__ == '__main__':
    app.run(threaded=True, port=5000)