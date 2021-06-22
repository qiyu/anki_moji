#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/20.
# Mail:yu.qi@qunar.com

import peewee

connect = peewee.SqliteDatabase("/Users/qiyu/Projects/qiyu/mojidicttool/data.db")


class WordModel(peewee.Model):
    title = peewee.CharField()
    target_id = peewee.CharField()
    target_type = peewee.IntegerField()
    excerpt = peewee.CharField(default='', null=True)
    spell = peewee.CharField(default='', null=True)
    accent = peewee.CharField(default='', null=True)
    pron = peewee.CharField(default='', null=True)
    review_count = peewee.IntegerField(default=0, null=True)
    first_review_time = peewee.DateTimeField(null=True)
    last_review_time = peewee.DateTimeField(null=True)
    next_review_time = peewee.DateTimeField(null=True)

    # 将表和数据库连接
    class Meta:
        database = connect


WordModel.create_table()
