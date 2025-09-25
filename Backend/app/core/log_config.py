import os
import sys
import logging
from typing import Any, Dict
from loguru import logger
from dotenv import load_dotenv

# Define colors for log levels
LEVEL_COLORS = {
    "DEBUG": "<blue>{level}</blue>",
    "INFO": "<green>{level}</green>",
    "WARNING": "<yellow>{level}</yellow>",
    "ERROR": "<red>{level}</red>",
    "CRITICAL": "<red>{level}</red>",
}

load_dotenv()

# Custom format for log messages
def custom_format(record: Dict[str, Any]) -> str:
    rel_file = os.path.relpath(record["file"].path)
    level_name = record["level"].name
    level_colored = LEVEL_COLORS.get(level_name, "{level}")

    # Format the log message
    return (
        f"{record['time'].strftime('%Y-%m-%d %H:%M:%S')} | "
        f"{level_colored:<8} | "
        f"{rel_file}:{record['line']}:{record['function']} - "
        f"{record['message']}\n"
    )


def setup_logging(log_level: str = "DEBUG") -> None:
    """
    Setup Loguru logging for the project.
    Creates console logs, file logs, error logs, and JSON structured logs.
    """
    # Map string level to both Loguru and stdlib logging levels
    level_name = str(log_level).upper()
    std_levels = {
        "TRACE": 5,
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    std_level = std_levels.get(level_name, logging.DEBUG)

    # Fallback to relative path if the environment variable is not set
    env_log_dir = os.getenv("LOG_DIR")
    if env_log_dir and env_log_dir.strip():
        log_dir = env_log_dir.strip()
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "../../logs")
    os.makedirs(log_dir, exist_ok=True)

    # Paths for different log files
    log_file_path = os.path.join(log_dir, "app.log")  # Main log file
    log_file_jsonl = os.path.join(log_dir, "app.jsonl")  # Main structured JSON log
    error_log_path = os.path.join(log_dir, "error.log")  # Separate error log file
    error_log_jsonl = os.path.join(log_dir, "error.jsonl")  # JSON error log

    logger.remove()

    logger.add(
        sys.stdout,
        format=custom_format,
        level=level_name,
        enqueue=True,  # Enable thread-safe logging
        backtrace=False,  # Reduce console noise
        diagnose=False,  # Reduce console noise
    )

    # Main application log (rotates when >50MB, keeps 10 days, compresses old logs)
    logger.add(
        log_file_path,
        format=custom_format,
        level=level_name,
        rotation="50 MB",
        retention="10 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
    )

    # Separate error log for easier debugging
    logger.add(
        error_log_path,
        format=custom_format,
        level="ERROR",
        rotation="25 MB",
        retention="30 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=True,  # Include full error info
    )

    # JSON structured logs for analytics tools
    logger.add(
        log_file_jsonl,
        level=level_name,
        rotation="75 MB",
        retention="7 days",
        compression="zip",
        serialize=True,
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )

    # JSON structured error logs for error analysis
    logger.add(
        error_log_jsonl,
        level="ERROR",
        rotation="50 MB",
        retention="21 days",
        compression="zip",
        serialize=True,
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )

    # Bridge stdlib logging (including Uvicorn/FastAPI) into Loguru
    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno
            frame, depth = logging.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(std_level)
    for noisy_logger in (
        "uvicorn",
        "uvicorn.error",
        # keep access logs off unless explicitly enabled
        # "uvicorn.access",
        "fastapi",
        "asyncio",
    ):
        logging.getLogger(noisy_logger).handlers = [InterceptHandler()]
        logging.getLogger(noisy_logger).propagate = False
        logging.getLogger(noisy_logger).setLevel(std_level)

    logger.info(f"Logging initialized with level: {level_name}")
    logger.info(f"Log directory: {os.path.abspath(log_dir)}")
