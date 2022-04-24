#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/17.
# Mail:qiyu.one@gmail.com
import logging
import os

import requests


from core import common


def save_tts_file(target_id, url):
    if common.no_anki_mode:
        logging.debug(f'虚拟保存文件, target_id={target_id}, url={url}')
        return
    from aqt import mw
    destination_folder = mw.col.media.dir()
    file_path = os.path.join(destination_folder, 'moji_' + target_id + '.mp3')
    if os.path.lexists(file_path):
        return file_path
    res = requests.get(url)
    print('save file ' + file_path)
    with open(file_path, 'wb') as f:
        f.write(res.content)
    return file_path
