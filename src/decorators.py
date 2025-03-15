from functools import wraps


def log(filename=None):
    """
    Декоратор для логирования выполнения функций.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log_message = ""
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok\n"
            except Exception as e:
                log_message = f"{func.__name__} error: {type(e).__name__}. " f"Inputs: {args}, {kwargs}\n"
                raise
            finally:
                if filename:
                    with open(filename, "a") as f:
                        f.write(log_message)
                else:
                    print(log_message.strip())
            return result

        return wrapper

    return decorator
