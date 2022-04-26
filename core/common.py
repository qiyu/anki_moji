import datetime
import time

no_anki_mode = False
interrupted = False


def retry(times=1, interval=1):
    def decorator(func):

        def target(*args, **kwargs):
            actual_times = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if actual_times <= times:
                        actual_times += 1
                        common_log(f'出现异常, {interval}秒后第{actual_times}次重试')
                        time.sleep(interval)
                    else:
                        common_log(f'重试{times}次后依然失败, 放弃重试')
                        raise e

        return target

    return decorator


def common_log(content):
    print(datetime.datetime.now().strftime('%Y-%m-%e %H:%M:%S') + ' anki_moji ' + content)
