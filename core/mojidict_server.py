#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/16.
# Mail:qiyu.one@gmail.com
from __future__ import annotations

import datetime
import json
import re
import time
from dataclasses import dataclass
from typing import Iterable, Union, Optional, List, Callable

import requests

from . import utils, common

URL_COLLECTION = 'https://api.mojidict.com/parse/functions/folder-fetchContentWithRelatives'
URL_WORD_DETAIL = 'https://api.mojidict.com/parse/functions/web-word-fetchLatest'
URL_EXAMPLE = 'https://api.mojidict.com/parse/functions/nlt-fetchExample'
URL_SENTENCES = 'https://api.mojidict.com/parse/functions/nlt-fetchManySentences'
URL_TTS = 'https://api.mojidict.com/parse/functions/tts-fetch'
URL_LOGIN = 'https://api.mojidict.com/parse/functions/login'
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

    @property
    def link(self):
        if self.target_type == 102:
            return "https://www.mojidict.com/details/" + self.target_id
        elif self.target_type == 103:
            return "https://www.mojidict.com/example/" + self.target_id
        elif self.target_type == 120:
            return "https://www.mojidict.com/sentence/" + self.target_id
        else:
            return ''


@dataclass
class MojiFolder:
    title: str
    target_id: str
    target_type: int
    parent: Optional[MojiFolder]

    @property
    def link(self):
        return "https://www.mojidict.com/collection/" + self.target_id


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
        self.should_retry: Optional[Callable] = None

    @utils.retry(times=3, check_should_retry=True)
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
                                 example.get('trans', ''),
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
                common.get_logger().info('process failed: ' + json.dumps(row.__dict__, ensure_ascii=True))
                raise e

    # 请求多个单词数据
    @utils.retry(times=3, check_should_retry=True)
    def get_words_data(self, target_ids: list):
        items = []
        for target_id in target_ids:
            items.append({"objectId": target_id})

        self.pre_request('word_detail')
        rw = requests.post(URL_WORD_DETAIL, json={
            "g_os": "PCWeb",
            "itemsJson": items,
            "_SessionToken": self.session_token,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request('word_detail')

        if rw.status_code != 200:
            raise Exception('获取单词详情异常, ', rw.status_code)
        return utils.get((rw.json()), 'result')

    # 获取词性、释义和例句
    def get_word_details(self, target_ids: list):
        if not target_ids:
            return {}
        words_data = self.get_words_data(target_ids)
        details = {}
        for target_id in target_ids:
            # id 为 target_id 的单词的信息
            info = [result for result in words_data["result"] if result["objectId"] == target_id][0]
            # id 为 target_id 的单词的所有词性
            all_part_of_speech \
                = [part_of_speech for part_of_speech in words_data["105"] if part_of_speech["wordId"] == target_id]
            # id 为 target_id 的单词的所有中日双解
            all_subdetails = [subdetail for subdetail in words_data["104"] if subdetail["wordId"] == target_id]
            # id 为 target_id 的单词的所有例句和例句翻译
            all_examples = [example for example in words_data["103"] if example["wordId"] == target_id]
            # TODO 修改笔记获取方式，可以少发一次请求
            # id 为 target_id 的单词的所有笔记
            # all_notes = [note for note in words_data["300"] if note["targetId"] == target_id]

            isGrammar = utils.get(info, 'type') == 2  # 是否是语法

            # Anki中的词性字段HTML
            part_of_speech_html = ''
            #
            excerpt = utils.get(info, "excerpt") or ''

            if not isGrammar:
                # 语法无词性，字段留空

                # 用于存储该单词的所有词性(虽然新版似乎都是只有一个词性了)
                part_of_speech_title_A_list = []  # 动词活用显示为：五段/一段/カ变/サ变
                part_of_speech_title_B_list = []  # 动词活用显示为：一类/二类/三类
                color_word_tag_underline_list = []  # 词性下划线的颜色（单个元素为rgb字符串，如："rgb(217, 212, 247)"）
                for part_of_speech in all_part_of_speech:
                    sub_part_of_speech_title_list = []
                    jita = utils.get(part_of_speech, "jita")
                    katuyou = utils.get(part_of_speech, "katuyou")
                    part_of_speech_list = utils.get(part_of_speech, "partOfSpeech")
                    valid_part_of_speech_list = [part_of_speech for part_of_speech in part_of_speech_list if
                                                 part_of_speech is not None and 0 <= part_of_speech < 20]
                    color_word_tag_underline_list.append(
                        ["",
                         "rgb(0, 212, 247)",
                         "rgb(0, 212, 247)",
                         "rgb(240, 173, 176)",
                         "rgb(255, 169, 65)",
                         "rgb(135, 158, 92)",
                         "rgb(19, 194, 194)",
                         "rgb(255, 169, 65)",
                         "rgb(217, 212, 247)",
                         "rgb(240, 173, 176)",
                         "rgb(255, 169, 65)",
                         "rgb(255, 169, 65)",
                         "rgb(19, 194, 194)",
                         "rgb(19, 194, 194)",
                         "rgb(207, 3, 79)",
                         "rgb(240, 173, 176)",
                         "rgb(240, 173, 176)",
                         "rgb(240, 173, 176)",
                         "rgb(240, 173, 176)",
                         "rgb(255, 169, 65)"
                         ][valid_part_of_speech_list[0] if len(valid_part_of_speech_list) > 0 and
                                                           valid_part_of_speech_list[0] is not None else 1])
                    if len(valid_part_of_speech_list) > 0:
                        for partOfSpeech in valid_part_of_speech_list:
                            if partOfSpeech != 8 or not jita:  # 动词会显示jita的“自动”/“他动”/“自他动”，因此不显示“动”
                                sub_part_of_speech_title_list.append({
                                                                         0: "无",
                                                                         1: "名",
                                                                         2: "代名",
                                                                         3: "形动",
                                                                         4: "连体",
                                                                         5: "副",
                                                                         6: "接续",
                                                                         7: "感动",
                                                                         8: "动",
                                                                         9: "形",
                                                                         10: "助动",
                                                                         11: "助",
                                                                         12: "接头",
                                                                         13: "接尾",
                                                                         14: "惯用",
                                                                         15: "形动ナリ",
                                                                         16: "形动タリ",
                                                                         17: "形ク",
                                                                         18: "形シク",
                                                                         19: "枕词"
                                                                     }[partOfSpeech])
                        if jita:
                            sub_part_of_speech_title_list.append({
                                                                     0: "无",
                                                                     1: "自动",
                                                                     2: "他动",
                                                                     3: "自他动"
                                                                 }[jita])
                        if katuyou:
                            sub_part_of_speech_title_list.append({
                                                                     0: "无",
                                                                     1: "五段",
                                                                     2: "一段",
                                                                     3: "カ变",
                                                                     4: "サ变",
                                                                     5: "ザ变",
                                                                     6: "文言四段",
                                                                     7: "文言上二段",
                                                                     8: "文言下二段",
                                                                     9: "文言カ变",
                                                                     10: "文言サ变",
                                                                     11: "文言ザ变",
                                                                     12: "文言ナ变",
                                                                     13: "文言ラ变"
                                                                 }[katuyou])
                        part_of_speech_title_A_list.append("·".join(sub_part_of_speech_title_list))
                        if katuyou:
                            sub_part_of_speech_title_list.pop()
                            sub_part_of_speech_title_list.append({
                                                                     0: "无",
                                                                     1: "一类",
                                                                     2: "二类",
                                                                     3: "三类",
                                                                     4: "三类",
                                                                     5: "ザ变",
                                                                     6: "文言四段",
                                                                     7: "文言上二段",
                                                                     8: "文言下二段",
                                                                     9: "文言カ变",
                                                                     10: "文言サ变",
                                                                     11: "文言ザ变",
                                                                     12: "文言ナ变",
                                                                     13: "文言ラ变"
                                                                 }[katuyou])
                        part_of_speech_title_B_list.append("·".join(sub_part_of_speech_title_list))
                    else:
                        # 通过excerpt获取词性
                        excerpt_match = re.match("\[([^[\]]*)\]", excerpt)
                        part_of_speech_text = excerpt_match.group()[1:-1] if excerpt_match else ""
                        part_of_speech_title_A_list.append(part_of_speech_text)
                        part_of_speech_title_B_list.append(part_of_speech_text)
                part_of_speech_html = ''.join([f'''
                <div class="word-speech" 
                    style="--color-word-tag-underline: {color_word_tag_underline_list[i]}"
                    a="{title_A}"
                    b="{part_of_speech_title_B_list[i]}"
                >
                    {title_A}
                </div>
                ''' for (i, title_A) in enumerate(part_of_speech_title_A_list)])

            # 用于存储该单词的所有释义
            subdetail_dict = {}
            # 单个释义结构如下:
            # key: subdetail_id
            # value:
            # {
            #     "title-zh": "xxx...",             # 中文释义
            #     "title-ja": "xxx...",             # 日文释义
            #     "conjunctions": [...],            # 接续
            #     "context-zh": "xxxxxxxxxx",       # 使用语境（中文）
            #     "context-ja": "xxxxxxxxxx",       # 使用语境（日文）
            #     "examples": {xxx}                 # 例句
            # }
            #
            # 单个例句结构如下：
            # key: example_id
            # value:
            # {
            #     "notationTitle-ja": "xxx",
            #     "title-zh": "xxx",
            # }
            for subdetail in all_subdetails:
                subdetail_id = utils.get(subdetail, "relaId")
                if subdetail_id not in subdetail_dict:
                    subdetail_dict[subdetail_id] = {
                        "title-zh": "",
                        "title-ja": "",
                        "conjunctions": [],
                        "context-zh": "",
                        "context-ja": "",
                        "examples": {}
                    }
                lang = utils.get(subdetail, "lang")
                title = utils.get(subdetail, "title") or ""
                context = utils.get(subdetail, "context") or ""
                conjunctions = utils.get(subdetail, "conjunctions") or []
                if lang == "zh-CN":
                    subdetail_dict[subdetail_id]["title-zh"] = title
                    subdetail_dict[subdetail_id]["context-zh"] = context
                elif lang == "ja":
                    subdetail_dict[subdetail_id]["title-ja"] = title
                    subdetail_dict[subdetail_id]["context-ja"] = context
                subdetail_dict[subdetail_id]["conjunctions"].extend(conjunctions)

            for example in all_examples:
                subdetail_id = utils.get(example, "subdetailsId")
                if subdetail_id not in subdetail_dict:
                    continue

                examples_dict = subdetail_dict[subdetail_id]["examples"]
                example_id = utils.get(example, "relaId")
                if example_id not in examples_dict:
                    examples_dict[example_id] = {
                        "notationTitle-ja": "",
                        "title-zh": "",
                    }
                lang = utils.get(example, "lang")
                notation_title = utils.get(example, "notationTitle") or ""
                title = utils.get(example, "title") or ""
                if lang == "zh-CN":
                    examples_dict[example_id]["title-zh"] = title
                elif lang == "ja":
                    examples_dict[example_id]["notationTitle-ja"] = notation_title

            # 单个元素为 单个释义+该释义下的所有例句 的HTML片段
            subdetail_container_html_list = []
            # 释义列表，用于生成trans_html
            trans_list = []
            for (subdetail_id, subdetail) in subdetail_dict.items():
                # 中日释义 + 接续 + 中日使用环境
                subdetail_header_container_html = ''
                trans_list_item = ''
                if subdetail["title-zh"]:
                    subdetail_header_container_html += \
                        f'''
                        <div class="column">
                            <img src="_ic_difinition_cn.svg" alt="中文icon" class="icon">
                            <span class="label">{subdetail["title-zh"]}</span>
                        </div>
                        '''
                    trans_list_item += subdetail["title-zh"] + '<br>'
                if subdetail["title-ja"]:
                    subdetail_header_container_html += \
                        f'''
                        <div class="column font-JP">
                            <img src="_ic_difinition_jp.svg" alt="日文icon" class="icon">
                            <span class="label">{subdetail["title-ja"]}</span>
                        </div>
                        '''
                    trans_list_item += subdetail["title-ja"] + ''
                trans_list.append(trans_list_item)
                if len(subdetail["conjunctions"]) > 0:
                    conjunctions_text = "<br>".join(
                        map(lambda conjunction: conjunction.replace("\\n", "<br>"), subdetail["conjunctions"]))
                    subdetail_header_container_html += \
                        f'''
                        <div class="column continue font-JP">
                            <img src="_icon-continue.webp" alt="接续" class="icon_continue">
                        </div>
                        <div class="column">{conjunctions_text}</div>
                        '''
                if subdetail["context-zh"] or subdetail["context-ja"]:
                    subdetail_header_container_html += \
                        f'''
                        <div class="column font-JP">
                            <img data-v-770d6cb9="" src="_icon-context.webp" alt="使用语境" class="icon_context">
                        </div>
                        '''
                if subdetail["context-zh"]:
                    subdetail_header_container_html += \
                        f'''
                        <div class="column">
                            <img src="_ic_difinition_cn.svg" alt="中文icon" class="icon">
                            <span class="label">{subdetail["context-zh"]}</span>
                        </div>
                        '''
                if subdetail["context-ja"]:
                    subdetail_header_container_html += \
                        f'''
                        <div class="column context_ja font-JP">
                            <img data-v-770d6cb9="" src="_ic_difinition_jp.svg" alt="日文icon" class="icon">
                            <span class="label">{subdetail["context-zh"]}</span>
                        </div>
                        '''

                # subdetail_header_container_html + 折叠例句按钮 的HTML片段
                subdetail_header_html = \
                    f'''
                    <div class="subdetail-container{' noneChildren' if len(subdetail['examples']) == 0 else ''}">
                    {subdetail_header_container_html}
                    </div>
                    <div class="subdetail_icon_wrap">
                        <i class="subdetail_icon iconfont icon-arrow-right"></i>
                    </div>
                    '''
                example_details_html_list = []
                for (example_id, example) in subdetail["examples"].items():
                    example_details_html_list.append(f'''
                    <div class="example-inner">
                        <div class="example-info">
                            <div class="line1 font-JP haveNotation">{example["notationTitle-ja"]}</div>
                            <div class="line2">{example["title-zh"]}</div>
                        </div>
                    </div>
                    ''')
                examplesContainer_html = ''.join([f'''
                <div class="example-details">
                    {example_details_html}
                </div>''' for example_details_html in example_details_html_list])

                subdetail_container_html_list.append(f'''
                <div subdetailId="{subdetail_id}" class="subdetail_header">{subdetail_header_html}</div>
                <div class="examplesContainer" style="--exampleNum: {len(subdetail["examples"])}">{examplesContainer_html}</div>
                ''')

            subdetail_containers_html = ''.join([f'''
            <div class="subdetail_container">
                {subdetail_container_html}
            </div>''' for subdetail_container_html in subdetail_container_html_list])
            # 所有释义+例句 HTML片段
            paraphrase_html = \
                f'''
                <div class="paraphrase-header">
                    <span class="title">{"详解" if isGrammar else "释义"}</span>
                    <span class="btn-fold">
                        <i class="iconfont iconic_toolbar_hide"></i>
                    </span>
                </div>
                {subdetail_containers_html}
                '''

            # TODO 关联词 但需要多发送一次请求
            # has_related = utils.get(info, "hasRelated") or False
            conjunctive_html = ''

            examples_html = \
                f'''
                <div class="paraphrase">{paraphrase_html}</div>
                <div class="conjunctive">{conjunctive_html}</div>
                '''

            pron = utils.get(info, "pron") or ''
            romaji = utils.get(info, "romaji_hepburn_CN") or ''
            tags = (utils.get(info, "tags") or '').replace("#", "·")
            pron_html = f'<span pron="{pron}" romaji="{romaji}" tag="{tags}">{pron}</span>'

            trans_html = '<ol>' \
                         + ''.join([f'<li>{trans}</li>' for trans in trans_list]) \
                         + '</ol>'

            details[target_id] = {
                'part_of_speech': part_of_speech_html,
                'trans': trans_html,
                'examples': examples_html,
                'excerpt': excerpt,
                'spell': utils.get(info, "spell") or '',
                'accent': utils.get(info, "accent") or '',
                'pron': pron_html,
            }
        return details

    # 获取单个例句(指词单中加的单句，非单个单词的例句列表)
    @utils.retry(times=3, check_should_retry=True)
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

    @utils.retry(times=3, check_should_retry=True)
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

    @utils.retry(times=3, check_should_retry=True)
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

    @utils.retry(times=3, check_should_retry=True)
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

    @utils.retry(times=3, check_should_retry=True)
    def get_file(self, url):
        self.pre_request('tts_file')
        res = requests.get(url, timeout=(5, 5))
        self.post_request('tts_file')

        if res.status_code != 200:
            raise Exception(f'获取单词发音文件异常, {url}')
        return res.content

    def login(self, passwd, email=None, countryCode=None, mobile=None):
        self.pre_request('login')
        r = requests.post(URL_LOGIN, json={
            'email': email,
            'countryCode': countryCode,
            'mobile': mobile,
            'passwd': passwd,
            "_ApplicationId": APPLICATION_ID,
            "_InstallationId": INSTALLATION_ID,
            "_ClientVersion": CLIENT_VERSION
        }, headers=headers, timeout=(5, 5))
        self.post_request('login')

        self.session_token = utils.get(r.json(), 'result.result.token')
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
                if utils.get(row, 'target') is None:
                    item.invalid = True
                items.append(item)

            self.parse_rows(items, moji_folder)

            for item in items:
                yield item

            page_index += 1
            # 当dir_id为空时total_page始终为0
            if not rows or (dir_id and page_index > total_page):
                break

    def get_one(self, title: str, target_id: str, target_type: int) -> MojiCollectionItem:
        item = MojiCollectionItem(title, target_id, target_type)
        self.parse_rows([item])
        return item
