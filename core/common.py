import logging
import time

no_anki_mode = False


def retry(times=1):
    def decorator(func):

        def target(*args, **kwargs):
            actual_times = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if actual_times <= times:
                        actual_times += 1
                        logging.debug(f'出现异常, 1秒后第{actual_times}重试')
                        time.sleep(1)
                    else:
                        logging.debug(f'重试{times}次依然失败, 放弃重试')
                        raise e

        return target

    return decorator
