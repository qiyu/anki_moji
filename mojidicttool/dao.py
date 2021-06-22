#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/20.
# Mail:yu.qi@qunar.com
from dataclasses import asdict
from datetime import datetime, timedelta

from pydash import omit

from mojidicttool.model import Word
from mojidicttool.peewee_db import WordModel


def query_all():
    return list(map(__to_word, WordModel.select().dicts().execute()))


def insert(word):
    WordModel.insert(asdict(word)).execute()


def delete(target_id):
    WordModel.delete().where(WordModel.target_id == target_id).execute()


def __to_word(d):
    return Word(**omit(d, 'id'))


def review_word(word: Word, reset=False):
    if word.review_count == 0:
        word.first_review_time = datetime.now()
    if reset:
        review_count = 0
    else:
        review_count = word.review_count + 1

    WordModel.update(
        review_count=review_count,
        first_review_time=word.first_review_time,
        last_review_time=datetime.now(),
        next_review_time=datetime.now() + timedelta(hours=(pow(2, review_count) - 1) * 12)
    ).where(
        WordModel.target_id == word.target_id
    ).execute()
