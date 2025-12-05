import logging
import inspect


class AppLogger:
    def __init__(self) -> None:
        self.logger = logging.getLogger("application_logger")
        self.logger.setLevel(logging.DEBUG)

        log_format = "%(levelname)s - %(asctime)s - %(message)s"
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _get_caller_info(self) -> str:
        frame = inspect.stack()[2]
        module = inspect.getmodule(frame[0])
        filename = module.__file__ if module else None

        if filename:
            relative_filename = filename.split("order_fast_api/")[-1]
        else:
            relative_filename = "Unknown"

        line = frame.lineno
        return f"{relative_filename}:{line}"

    def info(self, message: str) -> None:
        caller = self._get_caller_info()
        self.logger.info("%s : %s", caller, message)

    def error(self, message: str) -> None:
        caller = self._get_caller_info()
        self.logger.error("%s : %s", caller, message)

    def warning(self, message: str) -> None:
        caller = self._get_caller_info()
        self.logger.warning("%s : %s", caller, message)
