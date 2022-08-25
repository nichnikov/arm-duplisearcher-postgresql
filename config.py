import logging.config
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=os.path.join(ROOT_DIR, "logger.ini"), disable_existing_loggers=False)

SHARD_SIZE = 45000
VOCABULARY_SIZE = 35000
DB_PATH = os.getenv("DB_PATH", ":memory:")
# DB_PATH = os.path.join(ROOT_DIR, "data/queries.db")
