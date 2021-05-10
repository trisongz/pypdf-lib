import sys
import logging
import threading

_lock = threading.Lock()
_logger_handler = None

def _configure_logger():
    global _logger_handler
    with _lock:
        if _logger_handler:
            return
        _logger_handler = logging.getLogger(__name__)
        _logger_handler.setLevel(logging.INFO)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        _logger_handler.addHandler(console_handler)
        _logger_handler.propagate = False

def get_logger():
    _configure_logger()
    return _logger_handler