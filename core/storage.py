#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/17.
# Mail:qiyu.one@gmail.com
import os
from aqt import mw

from . import common


def save_tts_file(file_path, content):
    common.get_logger().info('save file, path: ' + file_path)
    with open(file_path, 'wb') as f:
        f.write(content)
    return file_path


def has_file(file_path):
    return os.path.lexists(file_path)


def get_file_path(target_id):
    destination_folder = mw.col.media.dir()
    file_path = os.path.join(destination_folder, 'moji_' + target_id + '.mp3')
    return file_path
