import logging
import time
from functools import wraps

log = logging.getLogger(__name__)


def retry(retries=3, delay=5, backoff=2):
    """
    A decorator to retry a function if it raises an exception.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    log.error(
                        f"Exception occurred: {e}, retrying in {current_delay} seconds..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
            log.error(f"Function {func.__name__} failed after {retries} retries.")
            raise

        return wrapper

    return decorator
