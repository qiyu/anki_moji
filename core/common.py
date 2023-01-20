import datetime
import time

no_anki_mode = False


def retry(times=1, interval=1):
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
                    else:
                        common_log(f'failed after {times} retries')
                        raise e

        return target

    return decorator


def common_log(content):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' anki_moji ' + content)
