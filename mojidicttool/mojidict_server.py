#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/16.
# Mail:yu.qi@qunar.com

from pydash import get
from requests import post

from mojidicttool.model import Word

URL_COLLECTION = 'https://api.mojidict.com/parse/functions/folder-fetchContentWithRelatives'
URL_TTS = 'https://api.mojidict.com/parse/functions/fetchTts_v2'
CLIENT_VERSION = 'js2.12.0'
SESSION_TOKEN = 'r:b413ba29930103a860f1b6aef7bec60e'
APPLICATION_ID = 'E62VyFVLMiW7kvbtVq3p'
INSTALLATION_ID = '7d959a18-48c4-243c-7486-632147466544'


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
    r = post(URL_COLLECTION,
             json={"fid": "", "pageIndex": page_index, "count": 30, "sortType": 0, "_SessionToken": SESSION_TOKEN,
                   "_ApplicationId": APPLICATION_ID, "_InstallationId": INSTALLATION_ID,
                   "_ClientVersion": CLIENT_VERSION})
    data = (r.json())
    rows = get(data, 'result.result')
    mojiwords = []
    for row in rows:
        target = (get(row, 'target'))
        if row['targetType'] != 102:
            continue
        word = Word(row['title'], row['targetId'], row['targetType'], get(target, 'excerpt'), get(target, 'spell'),
                    get(target, 'accent'),
                    get(target, 'pron'), 0, None, None, None)
        mojiwords.append(word)
    return mojiwords


def get_tts(tar_id, tar_type):
    r = post(URL_TTS,
             json={'tarId': tar_id, 'tarType': tar_type, "_SessionToken": SESSION_TOKEN,
                   "_ApplicationId": APPLICATION_ID, "_InstallationId": INSTALLATION_ID,
                   "_ClientVersion": CLIENT_VERSION})
    return get(r.json(), 'result.result.url')
