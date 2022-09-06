import logging.config
import os

import dotenv

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=os.path.join(ROOT_DIR, "logger.ini"), disable_existing_loggers=False)

SHARD_SIZE = 45000
VOCABULARY_SIZE = 35000
DEV_URL = "http://srv01.lingua.dev.msk2.sl.amedia.tech:8000/api"

dotenv.load_dotenv()

QUERIES_DB = os.getenv("QUERIES_DB")
