import os

from dotenv import load_dotenv

load_dotenv()

PORT = 4000
ENGINE = os.environ['ENGINE']
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'qwerty' 