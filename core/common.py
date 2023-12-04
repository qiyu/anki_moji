import datetime
import time

moji_server = None


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
                        common_log(f'execute function {func.__name__} failed, '
                                   f'retry in {interval} seconds({actual_times}st)')
                        time.sleep(interval)
                    elif check_should_retry and _exec_should_retry_func(*args, **kwargs):
                        common_log(f'execute function {func.__name__} failed, '
                                   f'retry by check_should_retry')
                    else:
                        common_log(f'failed after {times} retries')
                        raise e

        return target

    return decorator


def _exec_should_retry_func(*args, **_):
    if len(args) > 0:
        should_retry = getattr(args[0], 'should_retry', None)
        return should_retry and should_retry()
    return False


def common_log(content):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' anki_moji ' + content)
