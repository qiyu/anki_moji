import time

from . import common


def get(obj: dict, path: str):
    if obj is None:
        return None
    field_names = path.split('.')
    current = obj
    for field_name in field_names:
        current = current.get(field_name)
        if current is None:
            return None
    return current


def retry(times=1, interval=1, check_should_retry=False):
    def decorator(func):

        def target(*args, **kwargs):
            actual_times = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    actual_times += 1
                    if actual_times <= times:
                        common.get_logger().info(f'execute function {func.__name__} failed, '
                                                 f'retry in {interval} seconds({actual_times}st)')
                        time.sleep(interval)
                    elif check_should_retry and _exec_should_retry_func(*args, **kwargs):
                        common.get_logger().info(f'execute function {func.__name__} failed, '
                                                 f'retry by check_should_retry')
                    else:
                        common.get_logger().info(f'failed after {times} retries')
                        raise e

        return target

    return decorator


def _exec_should_retry_func(*args, **_):
    if len(args) > 0:
        should_retry = getattr(args[0], 'should_retry', None)
        return should_retry and should_retry()
    return False
