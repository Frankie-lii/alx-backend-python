import functools

def log_queries():
        def decorator(func):
                    @functools.wraps(func)
                            def wrapper(*args, **kwargs):
                                            print(f"[LOG] About to execute SQL query in '{func.__name__}'...")
                                                        result = func(*args, **kwargs)
                                                                    print(f"[LOG] Done executing SQL query in '{func.__name__}'.")
                                                                                return result
                                                                                    return wrapper
                                                                                    return decorator

