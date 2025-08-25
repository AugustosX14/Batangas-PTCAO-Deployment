# File: /Users/antonio/Documents/development_folder/Batangas_PTCAO/Batangas_PTCAO/src/config.py
import os
from urllib.parse import urlparse

class Config:
    # Get database URL from environment or use default
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Parse the database URL for production
        url = urlparse(database_url)
        SQLALCHEMY_DATABASE_URI = database_url
        
        # Handle postgres:// vs postgresql:// issue
        if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    else:
        # Development database
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/batangas_ptcao'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = False
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
