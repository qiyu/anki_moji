#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/16.
# Mail:qiyu.one@gmail.com
import datetime
import time
from dataclasses import dataclass
from typing import Iterable

import requests

from . import utils
from .common import retry, common_log

URL_COLLECTION = 'https://api.mojidict.com/parse/functions/folder-fetchContentWithRelatives'
URL_TTS = 'https://api.mojidict.com/parse/functions/tts-fetch'
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


@dataclass
class MojiFolder:
    title: str
    target_id: str
    target_type: str


class MojiServer:
    def __init__(self):
        self.session_token = None
        self.last_request = None

    @retry(times=3)
    def fetch_from_server(self, dir_id, page_index):
        self.pre_request()
        r = requests.post(URL_COLLECTION, json={
            "fid": dir_id, "pageIndex": page_index, "count": 30, "sortType": 0,
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request()
        if r.status_code != 200:
            raise Exception(f'获取单词列表异常, {dir_id}, {page_index}')
        data = (r.json())
        rows = utils.get(data, 'result.result')
        mojiwords = []
        if not rows:
            common_log(f'获取单词列表为空或单词列表不存在，dir_id：{dir_id}，page_index：{page_index}')
            return mojiwords

        for row in rows:
            target = (utils.get(row, 'target'))
            if row['targetType'] == 102:
                mojiwords.append(
                    MojiWord(row['title'],
                             row['targetId'],
                             row['targetType'],
                             utils.get(target, 'excerpt') or '',
                             utils.get(target, 'spell') or '',
                             utils.get(target, 'accent') or '',
                             utils.get(target, 'pron') or ''))
            elif row['targetType'] == 1000:
                mojiwords.append(
                    MojiFolder(row['title'],
                               row['targetId'],
                               row['targetType']))
        return mojiwords

    @retry(times=3)
    def get_tts_url(self, word: MojiWord):
        self.ensure_login()
        self.pre_request()
        r = requests.post(URL_TTS, json={
            'g_os':'PCWeb',
            'tarId': word.target_id,
            'tarType': word.target_type,
            'voiceId': 'f000',
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request()
        if r.status_code != 200:
            raise Exception(f'获取单词发音文件地址异常, {word.target_id}')
        return utils.get(r.json(), 'result.result.url')

    @retry(times=3)
    def get_file(self, url):
        self.pre_request()
        res = requests.get(url, timeout=(5, 5))
        self.post_request()
        if res.status_code != 200:
            raise Exception(f'获取单词发音文件异常, {url}')
        return res.content

    def ensure_login(self):
        if not self.session_token:
            raise Exception('未登录')

    def login(self, username, password):
        self.pre_request()
        r = requests.post(URL_LOGIN, json={
            'username': username,
            'password': password,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request()
        self.session_token = utils.get(r.json(), 'sessionToken')
        if not self.session_token:
            raise Exception('登录失败')


    def pre_request(self):
        if self.last_request is not None and datetime.datetime.now().timestamp() - self.last_request < 0.6:
            time.sleep(1)

    def post_request(self):
        self.last_request = datetime.datetime.now().timestamp()

    def get_tts_url_and_download(self, word: MojiWord):
        url = self.get_tts_url(word)
        return self.get_file(url)

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
