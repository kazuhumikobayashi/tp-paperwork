DEBUG = False
TESTING = False

# Google Cloud Project ID
PROJECT_ID = 'tp-paperwork-development'

# CloudSQL & SQLAlchemy configuration
HOST = '35.187.201.221'
PORT = '3306'
USER = 'admin_user'
PASSWORD = 'admin_user'
DATABASE = 'tp_paperwork'
SQLALCHEMY_DATABASE_URI = (
    'mysql://{user}:{password}@{host}:{port}/{database}').format(
        user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY = 'development key'

# Google Cloud Storage and upload settings.
CLOUD_STORAGE_BUCKET = 'tp-paperwork-bucket-development'
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'xlsx', 'xls'}
