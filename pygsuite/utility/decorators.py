import time
from functools import wraps
from types import MethodType
from typing import Optional, Tuple, Union, Type


class lazy_property(object):
    def __init__(self, fget):
        self.fget = fget
        self.func_name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj, self.func_name, value)

        setattr(obj, "_method_{}".format(self.func_name), MethodType(self.fget, obj))
        return value


def safe_property(f):
    @property
    def wrapper(self, *args, **kwargs):
        if len(self._change_queue) > 0:
            self.flush()
        return f(self, *args, **kwargs)

    return wrapper


def retry(  # noqa: C901
    exceptions: Union[Type[Exception], Tuple[Type[Exception]]],
    tries: int = 4,
    delay: int = 3,
    backoff: int = 2,
    fatal_exceptions: Optional[Tuple] = None,
    logger=None,
):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """
    fatal_exceptions = fatal_exceptions or ()

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except fatal_exceptions as e:
                    if logger:
                        logger.error(f"Fatal exception, not retrying {str(e)}")
                    raise e
                except exceptions as e:
                    msg = "{}, Retrying in {} seconds...".format(e, mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry

    return deco_retry
