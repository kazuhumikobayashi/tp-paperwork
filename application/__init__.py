import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_bcrypt import Bcrypt
from flask_sslify import SSLify
from flask_sqlalchemy import SQLAlchemy
import pymysql

from application.blueprint import register
from application.viewhelper import my_filter

pymysql.install_as_MySQLdb()


app = Flask(__name__, template_folder='../templates', static_folder='../static')

config_name = os.getenv('FLASK_CONFIGURATION', 'local')
app.config.from_object('config.' + config_name)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
sslify = SSLify(app)

register(app)
my_filter(app)


@app.before_request
def before_request():
    # セッションに user が保存されている (= ログイン済み)
    if session.get('user') is not None:
        return
    # ログインページへの移動はそのまま
    if request.path == '/login':
        return
    # staticへのリクエストはそのまま
    if request.path.count('/static/'):
        return
    return redirect(url_for('login.login'))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
