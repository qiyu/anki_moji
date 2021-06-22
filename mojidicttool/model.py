#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/03/17.
# Mail:yu.qi@qunar.com
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Word:
    title: str
    target_id: str
    target_type: int
    excerpt: str
    spell: str
    accent: str
    pron: str
    review_count: int
    first_review_time: Optional[datetime]
    last_review_time: Optional[datetime]
    next_review_time: Optional[datetime]
