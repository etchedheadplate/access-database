import logging

from src.config import Settings

settings = Settings()  # type: ignore[call-arg]


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
# handler.addFilter(PrefixFilter(settings.SERVICE_NAME))

logger.addHandler(handler)

logger.info("Service started")
