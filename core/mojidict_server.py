#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/16.
# Mail:yu.qi@qunar.com
from dataclasses import dataclass
from typing import Iterable

import requests

import utils
from mojidicttool.model import Word

URL_COLLECTION = 'https://api.mojidict.com/parse/functions/folder-fetchContentWithRelatives'
URL_TTS = 'https://api.mojidict.com/parse/functions/fetchTts_v2'
URL_LOGIN = 'https://api.mojidict.com/parse/login'

CLIENT_VERSION = 'js2.12.0'
APPLICATION_ID = 'E62VyFVLMiW7kvbtVq3p'
INSTALLATION_ID = '7d959a18-48c4-243c-7486-632147466544'


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

    def fetch_all_from_server(self) -> Iterable[MojiWord]:
        self.ensure_login()
        page_index = 1
        while True:
            mojiwords = self.fetch_from_server(page_index)
            for mojiword in mojiwords:
                yield mojiword
            page_index += 1
            if not mojiwords:
                break

    def fetch_from_server(self, page_index):
        r = requests.post(URL_COLLECTION, json={
            "fid": "", "pageIndex": page_index, "count": 30, "sortType": 0,
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION})
        data = (r.json())
        rows = utils.get(data, 'result.result')
        mojiwords = []
        for row in rows:
            target = (utils.get(row, 'target'))
            if row['targetType'] != 102:
                continue
            word = Word(row['title'],
                        row['targetId'],
                        row['targetType'],
                        utils.get(target, 'excerpt'),
                        utils.get(target, 'spell'),
                        utils.get(target, 'accent'),
                        utils.get(target, 'pron'))
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
        })
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
        })
        self.session_token = utils.get(r.json(), 'sessionToken')


server = MojiServer()
server.login('qiyu.one@gmail.com', '11301127')
for i in server.fetch_all_from_server():
    print(server.get_tts_url(i))
