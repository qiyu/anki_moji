#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/17.
# Mail:yu.qi@qunar.com
import os

import requests
from aqt import mw


def save_tts_file(target_id, url):
    if mw is None:
        return
    destination_folder = mw.col.media.dir()
    file_path = os.path.join(destination_folder, 'moji_' + target_id + '.mp3')
    if os.path.lexists(file_path):
        return file_path
    res = requests.get(url)
    print('save file ' + file_path)
    with open(file_path, 'wb') as f:
        f.write(res.content)
    return file_path
