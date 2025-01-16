import os
import sys
import json
from loguru import logger


class StdOutSink:
    def __init__(self):
        pass

    @staticmethod
    def json_formatter(record):
        log = {
            "timestamp": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
            "level": record["level"].name,
            "message": record["message"],
            "module": record["module"],
            "log_id": record["extra"].get("log_id", "N/A")
        }
        return json.dumps(log, ensure_ascii=False)

    def write(self, message):
        record = message.record
        formatted_message = self.json_formatter(record)
        sys.stdout.write(formatted_message + "\n")


def config_log_to_file(log_dir: str, filename: str, retention_day: int):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_format = f'{log_dir}/{filename}'
    file_format += '_{time:YYYY-MM-DD}.log'
    log_format = 'Log {time} - {level} - {message}'
    retention_period = f'{retention_day} days'
    logger.add(
        file_format,  # Path to the log file
        format=log_format,
        level="INFO",  # Log level
        enqueue=True,
        rotation="00:00",
        retention=retention_period,  # Optional: Retain logs for 10 days
        compression="zip"  # Optional: Compress rotated files
    )

def config_logger(log_dir: str, filename: str, is_log_to_stdout: bool, is_log_to_file: bool, log_retention: int):
    logger.remove()
    if is_log_to_stdout:
        logger.add(
            StdOutSink(),
            level="INFO",
            enqueue=True,
            serialize=False,
            backtrace=True,
            diagnose=True
        )
    if is_log_to_file:
        config_log_to_file(log_dir, filename, log_retention)