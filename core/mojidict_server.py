#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/16.
# Mail:qiyu.one@gmail.com
from __future__ import annotations

import datetime
import json
import time
from dataclasses import dataclass
from typing import Iterable, Union, Optional, List

import requests

from . import utils
from .common import retry, common_log

URL_COLLECTION = 'https://api.mojidict.com/parse/functions/folder-fetchContentWithRelatives'
URL_WORD_DETAIL = 'https://api.mojidict.com/parse/functions/nlt-fetchManyLatestWords'
URL_EXAMPLE = 'https://api.mojidict.com/parse/functions/nlt-fetchExample'
URL_SENTENCES = 'https://api.mojidict.com/parse/functions/nlt-fetchManySentences'
URL_TTS = 'https://api.mojidict.com/parse/functions/tts-fetch'
URL_LOGIN = 'https://api.mojidict.com/parse/login'
URL_USER_NOTE = 'https://api.mojidict.com/parse/functions/getNote'

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
    part_of_speech: str
    trans: str
    examples: str
    parent: Optional[MojiFolder]


@dataclass
class MojiFolder:
    title: str
    target_id: str
    target_type: int
    parent: Optional[MojiFolder]


class MojiCollectionItem:

    def __init__(self, title: str, target_id: str, target_type: int,
                 skipped: bool = False,
                 ):
        """
        :param title:
        :param target_id:
        :param target_type:
        :param skipped: 表示应该跳过处理，比如已导入过的单词
        """
        self.title = title
        self.target_id = target_id
        self.target_type = target_type
        self.skipped = skipped
        self.invalid: bool = False
        self.result_value: Optional[Union[MojiWord, MojiFolder]] = None


class MojiServer:
    def __init__(self):
        # 记录登录的token
        self.session_token = None
        # 记录生成登录token的时间
        self.session_token_datetime = None
        # 记录上次请求完成的时间，保证多次请求接口之间的间隔，防止请求过快
        self.last_requests = {}

    @retry(times=3)
    def fetch_from_server(self, dir_id, page_index):
        self.pre_request('fetch_from_server')
        r = requests.post(URL_COLLECTION, json={
            "fid": dir_id, "pageIndex": page_index, "count": 30, "sortType": 0,
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request('fetch_from_server')

        if r.status_code != 200:
            raise Exception(f'获取单词列表异常, {dir_id}, {page_index}')
        data = (r.json())
        rows = utils.get(data, 'result.result')
        total_page = utils.get(data, 'result.totalPage') or 0
        if not rows:
            return total_page, []

        return total_page, rows

    def parse_rows(self, rows: List[MojiCollectionItem], parent_moji_folder=None):
        word_ids = []
        sentence_ids = []
        for row in rows:
            if row.skipped or row.invalid:
                continue
            target_id = row.target_id
            target_type = row.target_type
            if target_type == 102:
                word_ids.append(target_id)
            elif target_type == 120:
                sentence_ids.append(target_id)
        word_details = self.get_word_details(word_ids)
        sentences = self.get_sentences(sentence_ids)
        for row in rows:
            if row.skipped or row.invalid:
                continue
            target_id = row.target_id
            target_type = row.target_type
            try:
                if target_type == 102:
                    detail = word_details.get(target_id)
                    if detail is None:
                        row.invalid = True
                        continue
                    row.result_value = (
                        MojiWord(row.title,
                                 target_id,
                                 target_type,
                                 detail['excerpt'],
                                 detail['spell'],
                                 detail['accent'],
                                 detail['pron'],
                                 detail['part_of_speech'] or '',
                                 detail['trans'] or '',
                                 detail['examples'] or '',
                                 parent_moji_folder))
                elif target_type == 103:
                    example = self.get_example(target_id)
                    if example is None:
                        row.invalid = True
                        continue
                    row.result_value = (
                        MojiWord(row.title,
                                 target_id,
                                 target_type,
                                 '',
                                 example['notationTitle'],
                                 '',
                                 '',
                                 '',
                                 example['trans'],
                                 '',
                                 parent_moji_folder))
                elif target_type == 120:
                    sentence = sentences[target_id]
                    if sentence is None:
                        row.invalid = True
                        continue
                    row.result_value = (
                        MojiWord(sentence['title'],
                                 target_id,
                                 target_type,
                                 '',
                                 sentence['notationTitle'],
                                 '',
                                 '',
                                 '',
                                 sentence.get('trans', ''),
                                 '',
                                 parent_moji_folder))
                elif target_type == 1000:
                    row.result_value = (
                        MojiFolder(row.title,
                                   target_id,
                                   target_type,
                                   parent_moji_folder))
            except Exception as e:
                common_log('process failed: ' + json.dumps(row, ensure_ascii=True))
                raise e

    # 请求多个单词数据
    @retry(times=3)
    def get_words_data(self, target_ids: list):
        items = []
        for target_id in target_ids:
            items.append({"objectId": target_id})

        self.pre_request('word_detail')
        rw = requests.post(URL_WORD_DETAIL, json={
            "g_os": "PCWeb",
            "itemsJson": items,
            "skipAccessories": False,
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request('word_detail')

        if rw.status_code != 200:
            raise Exception('获取单词详情异常, ', rw.status_code)
        return utils.get((rw.json()), 'result.result')

    # 获取词性、释义和例句
    def get_word_details(self, target_ids: list):
        if not target_ids:
            return {}
        words_data = self.get_words_data(target_ids)
        details = {}
        for word_data in words_data:
            parts_of_speech = {}
            trans = {}
            for detail in word_data['details']:
                parts_of_speech[detail['objectId']] = detail['title'].replace('#', '・')
            trans_html = '<ol>'
            for subdetail in word_data['subdetails']:
                trans_html += f'<li>{subdetail["title"]}</li>'
                trans[subdetail['objectId']] = {
                    'title': f"[{parts_of_speech[subdetail['detailsId']]}]{subdetail['title']}" if subdetail[
                                                                                                       'detailsId'] in parts_of_speech else
                    subdetail['title'],
                    'examples': []
                }
            trans_html += '</ol>'
            for example in word_data['examples']:
                if example['subdetailsId'] in trans:
                    trans[example['subdetailsId']]['examples'].append(
                        (example['notationTitle'], example.get('trans') or ''))
            examples_html = ''
            for trans_id in trans.keys():
                t = trans[trans_id]
                examples_html += f'<div class="word-trans" onclick="changeDisplay(`{trans_id}`)">{t["title"]}</div><div id="trans-{trans_id}">'
                for e in t['examples']:
                    examples_html += f'<div class="example-title">{e[0]}</div>'
                    examples_html += f'<div class="example-trans">{e[1]}</div>'
                examples_html += '</div>'
            details[word_data['word']['objectId']] = {
                'part_of_speech': " ".join(parts_of_speech.values()),
                'trans': trans_html,
                'examples': examples_html,
                'excerpt': utils.get(word_data, 'word.excerpt') or '',
                'spell': utils.get(word_data, 'word.spell') or '',
                'accent': utils.get(word_data, 'word.accent') or '',
                'pron': utils.get(word_data, 'word.pron') or '',
            }
        return details

    # 获取单个例句(指词单中加的单句，非单个单词的例句列表)
    @retry(times=3)
    def get_example(self, target_id):
        self.pre_request('example')
        r = requests.post(URL_EXAMPLE, json={
            "g_os": "PCWeb",
            "id": target_id,
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request('example')

        if r.status_code != 200:
            raise Exception('获取例句异常, ', r.status_code)
        return utils.get((r.json()), 'result.result')

    @retry(times=3)
    def get_sentences(self, target_ids: list):
        if not target_ids:
            return {}

        self.pre_request('sentences')
        r = requests.post(URL_SENTENCES, json={
            "g_os": "PCWeb",
            "ids": target_ids,
            "withExtra": True,
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request('sentences')

        if r.status_code != 200:
            raise Exception('获取句子异常, ', r.status_code)
        sentences = {}
        data_list = utils.get((r.json()), 'result.result')
        for data in data_list:
            sentences[data['objectId']] = data
        return sentences

    @retry(times=3)
    def get_user_note(self, word: MojiWord):
        self.pre_request('note')
        r = requests.post(URL_USER_NOTE, json={
            'g_os': 'PCWeb',
            "tarId": word.target_id,
            "tarType": word.target_type,
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request('note')

        if r.status_code != 200:
            raise Exception(f'获取用户笔记异常, {word.target_id}')
        note = utils.get((r.json()), 'result.result.content')
        return note if note is not None else ''

    @retry(times=3)
    def get_tts_url(self, word: MojiWord):
        self.pre_request('tts')
        r = requests.post(URL_TTS, json={
            'g_os': 'PCWeb',
            'tarId': word.target_id,
            'tarType': word.target_type,
            'voiceId': 'f000',
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request('tts')

        if r.status_code != 200:
            raise Exception(f'获取单词发音文件地址异常, {word.target_id}')
        return utils.get(r.json(), 'result.result.url')

    @retry(times=3)
    def get_file(self, url):
        self.pre_request('tts_file')
        res = requests.get(url, timeout=(5, 5))
        self.post_request('tts_file')

        if res.status_code != 200:
            raise Exception(f'获取单词发音文件异常, {url}')
        return res.content

    def login(self, username, password):
        self.pre_request('login')
        r = requests.post(URL_LOGIN, json={
            'username': username,
            'password': password,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request('login')

        self.session_token = utils.get(r.json(), 'sessionToken')
        if not self.session_token:
            raise Exception('登录失败')
        self.session_token_datetime = datetime.datetime.now()

    def session_valid(self):
        return (self.session_token is not None) and (self.session_token_datetime is not None) and (
                datetime.datetime.now() - self.session_token_datetime < datetime.timedelta(hours=1))

    def pre_request(self, request_key):
        # 防止因为请求速度过快，影响moji web服务器的正确响应
        last_request = self.last_requests.get(request_key)
        min_interval = 1.5
        if last_request is not None and datetime.datetime.now().timestamp() - last_request < min_interval:
            time.sleep(min_interval)

    def post_request(self, request_key):
        self.last_requests[request_key] = datetime.datetime.now().timestamp()

    def get_tts_url_and_download(self, word: MojiWord):
        url = self.get_tts_url(word)
        return self.get_file(url)

    def fetch_all_from_server(self, dir_id: str,
                              should_skip,
                              moji_folder: Optional[MojiFolder] = None) -> Iterable[MojiCollectionItem]:
        page_index = 1
        while True:
            total_page, rows = self.fetch_from_server(dir_id, page_index)

            items = []
            for row in rows:
                # 这里调用should_skip方法是为了提前识别出程序不需要处理的单词，减少parse_rows方法中向moji web请求的数据量
                item = MojiCollectionItem(row['title'], row['targetId'], row['targetType'],
                                          should_skip(row['targetId'], row['targetType']))
                # moji web中已经删除的数据也会在返回的数据列表中，但target为None，因此这个判断是为了排除已经删除的数据
                if row['targetType'] == 102 and utils.get(row, 'target') is None:
                    item.invalid = True
                items.append(item)

            self.parse_rows(items, moji_folder)

            for item in items:
                yield item

            page_index += 1
            # 当dir_id为空时total_page始终为0
            if not rows or (dir_id and page_index > total_page):
                break
