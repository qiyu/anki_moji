#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/16.
# Mail:yu.qi@qunar.com

import requests

import utils
from mojidicttool.model import Word

URL_COLLECTION = 'https://api.mojidict.com/parse/functions/folder-fetchContentWithRelatives'
URL_TTS = 'https://api.mojidict.com/parse/functions/fetchTts_v2'
URL_LOGIN = 'https://api.mojidict.com/parse/login'

CLIENT_VERSION = 'js2.12.0'
APPLICATION_ID = 'E62VyFVLMiW7kvbtVq3p'
INSTALLATION_ID = ''

SESSION_TOKEN = None


def fetch_all_from_server():
    page_index = 1
    all_mojiwords = []
    while True:
        mojiwords = fetch_from_server(page_index)
        all_mojiwords.extend(mojiwords)
        page_index += 1
        if not mojiwords:
            break
    return all_mojiwords


def fetch_from_server(page_index):
    r = requests.post(URL_COLLECTION,
                      json={"fid": "", "pageIndex": page_index, "count": 30, "sortType": 0,
                            "_SessionToken": SESSION_TOKEN,
                            "_ApplicationId": APPLICATION_ID, "_InstallationId": INSTALLATION_ID,
                            "_ClientVersion": CLIENT_VERSION})
    data = (r.json())
    rows = utils.get(data, 'result.result')
    mojiwords = []
    for row in rows:
        target = (utils.get(row, 'target'))
        if row['targetType'] != 102:
            continue
        word = Word(row['title'], row['targetId'], row['targetType'], utils.get(target, 'excerpt'),
                    utils.get(target, 'spell'),
                    utils.get(target, 'accent'),
                    utils.get(target, 'pron'), 0, None, None, None)
        mojiwords.append(word)
    return mojiwords


def get_tts(tar_id, tar_type):
    r = requests.post(URL_TTS,
                      json={'tarId': tar_id, 'tarType': tar_type, "_SessionToken": SESSION_TOKEN,
                            "_ApplicationId": APPLICATION_ID, "_InstallationId": INSTALLATION_ID,
                            "_ClientVersion": CLIENT_VERSION})
    return utils.get(r.json(), 'result.result.url')


def ensure_login():
    if not SESSION_TOKEN:
        raise Exception('未登录')


def login(username, password):
    r = requests.post(URL_LOGIN, json={
        'username': username,
        'password': password,
        "_ApplicationId": APPLICATION_ID,
        "_InstallationId": INSTALLATION_ID,
        "_ClientVersion": CLIENT_VERSION
    })
    return utils.get(r.json(), 'sessionToken')


print(login('qiyu.one@gmail.com', '11301127'))
