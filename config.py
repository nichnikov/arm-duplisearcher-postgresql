import logging.config
import os

import dotenv

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=os.path.join(ROOT_DIR, "logger.ini"), disable_existing_loggers=False)

SHARD_SIZE = 45000
VOCABULARY_SIZE = 35000

dotenv.load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_NAME")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
