SQLITE = 'sqlite:///project.db'
POSTGRESQL = 'postgresql://postgres:root@localhost/blogposts_db'

class Config:
    DEBUG = False
    SECRET_KEY = 'devblogpost'
    SQLALCHEMY_DATABASE_URI = POSTGRESQL
    CKEDITOR_PKG_TYPE = 'full'