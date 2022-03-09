#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/16.
# Mail:qiyu.one@gmail.com
from dataclasses import dataclass
from typing import Iterable

import requests

from . import utils

URL_COLLECTION = 'https://api.mojidict.com/parse/functions/folder-fetchContentWithRelatives'
URL_TTS = 'https://api.mojidict.com/parse/functions/fetchTts_v2'
URL_LOGIN = 'https://api.mojidict.com/parse/login'

CLIENT_VERSION = 'js3.4.1'
APPLICATION_ID = 'E62VyFVLMiW7kvbtVq3p'
INSTALLATION_ID = '5a06ea1a-8ce4-4943-9c59-dcac449812a9'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}


@dataclass
class MojiWord:
    title: str
    target_id: str
    target_type: int
    excerpt: str
    spell: str
    accent: str

    pron: str


class MojiServer:
    def __init__(self):
        self.session_token = None

    def fetch_all_from_server(self, dir_id) -> Iterable[MojiWord]:
        self.ensure_login()
        page_index = 1
        while True:
            mojiwords = self.fetch_from_server(dir_id, page_index)
            for mojiword in mojiwords:
                yield mojiword
            page_index += 1
            if not mojiwords:
                break

    def fetch_from_server(self, dir_id, page_index):
        r = requests.post(URL_COLLECTION, json={
            "fid": dir_id, "pageIndex": page_index, "count": 30, "sortType": 0,
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers)
        data = (r.json())
        rows = utils.get(data, 'result.result')
        mojiwords = []
        for row in rows:
            target = (utils.get(row, 'target'))
            if row['targetType'] != 102:
                continue
            word = MojiWord(row['title'],
                            row['targetId'],
                            row['targetType'],
                            utils.get(target, 'excerpt') or '',
                            utils.get(target, 'spell') or '',
                            utils.get(target, 'accent') or '',
                            utils.get(target, 'pron') or '')
            mojiwords.append(word)
        return mojiwords

    def get_tts_url(self, word: MojiWord):
        self.ensure_login()
        r = requests.post(URL_TTS, json={
            'tarId': word.target_id,
            'tarType': word.target_type,
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers)
        return utils.get(r.json(), 'result.result.url')

    def ensure_login(self):
        if not self.session_token:
            raise Exception('未登录')

    def login(self, username, password):
        r = requests.post(URL_LOGIN, json={
            'username': username,
            'password': password,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers)
        self.session_token = utils.get(r.json(), 'sessionToken')
        if not self.session_token:
            raise Exception('登录失败')
