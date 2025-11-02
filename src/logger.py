import logging
import os

from dotenv import load_dotenv

load_dotenv()


SERVICE_NAME = os.getenv("SERVICE_NAME", "Database")


class PrefixFilter(logging.Filter):
    def __init__(self, prefix: str):
        super().__init__()
        self.prefix = prefix

    def filter(self, record: logging.LogRecord):
        record.msg = f"[{self.prefix}] {record.msg}"
        return True


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
handler.setFormatter(formatter)

# Turned of so service name won't be doubled in Docker
# handler.addFilter(PrefixFilter(SERVICE_NAME))

logger.addHandler(handler)

logger.info("Service started")
