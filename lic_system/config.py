"""
LIC Management System - Flask Configuration
"""
import os
from datetime import timedelta

class Config:
    # ------- Security -------
    SECRET_KEY = os.environ.get('SECRET_KEY', 'lic-ms-super-secret-key-2026-change-in-prod')
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    # ------- MySQL -------
    MYSQL_HOST     = os.environ.get('MYSQL_HOST',     'localhost')
    MYSQL_USER     = os.environ.get('MYSQL_USER',     'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Jaydip@123')          # change to your MySQL password
    MYSQL_DB       = os.environ.get('MYSQL_DB',       'lic_management')
    MYSQL_PORT     = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_CURSORCLASS = 'DictCursor'

    # ------- Upload -------
    UPLOAD_FOLDER    = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

    # ------- Flash -------
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', '')  # Must be set in production env

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig
}
