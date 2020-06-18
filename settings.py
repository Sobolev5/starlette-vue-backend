import os

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from starlette.datastructures import Secret

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL", cast=str)
SECRET_KEY = config("SECRET_KEY", cast=Secret)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings)
JWT_PREFIX = config("JWT_PREFIX", cast=str)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str)
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# Mailer settings
MAILJET_API_KEY = config("MAILJET_API_KEY", cast=str)
MAILJET_API_SECRET = config("MAILJET_API_SECRET", cast=str)
USE_MAILER = config("USE_MAILER", cast=bool, default=False)
