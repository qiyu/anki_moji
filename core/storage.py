#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/17.
# Mail:yu.qi@qunar.com

import requests


def save_tts_file(file_path, url):
    res = requests.get(url)
    print('save file ' + file_path)
    with open(file_path, 'wb') as f:
        f.write(res.content)
    return file_path
