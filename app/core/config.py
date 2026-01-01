import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "PPLT")
    DEBUG = os.getenv("DEBUG", "False") == "True"

settings = Settings()
