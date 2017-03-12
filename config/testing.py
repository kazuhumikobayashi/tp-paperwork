import os

DEBUG = False
TESTING = True
WTF_CSRF_ENABLED = False

# Google Cloud Project ID
PROJECT_ID = 'tp-paperwork-development'

# CloudSQL & SQLAlchemy configuration
HOST = os.getenv('MYSQL_PORT_3306_TCP_ADDR', 'localhost')
PORT = os.getenv('MYSQL_PORT_3306_TCP_PORT', '3306')
USER = 'admin_user_test'
PASSWORD = 'admin_user_test'
DATABASE = 'tp_paperwork_test'
SQLALCHEMY_DATABASE_URI = (
    'mysql://{user}:{password}@{host}:{port}/{database}').format(
        user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY = 'testing key'

# Google Cloud Storage and upload settings.
CLOUD_STORAGE_BUCKET = 'tp-paperwork-bucket-testing'
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'xlsx', 'xls'}
