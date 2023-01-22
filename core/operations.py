#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2023/01/20.
# Mail:qiyu.one@gmail.com
# 依赖anki和mojidict_server模块
# 被gui和hooks模块依赖
from . import storage
from .mojidict_server import MojiServer


def update_note(moji_server: MojiServer, note, word, update_keys):
    from aqt import mw
    for key in update_keys:
        if key == 'note':
            user_note = moji_server.get_user_note(word)
            # 避免清空用户手动填入的内容
            if user_note:
                note[key] = user_note
        elif key == 'sound':
            note[key] = f'[sound:moji_{word.target_id}.mp3]'
            file_path = storage.get_file_path(word.target_id)
            content = moji_server.get_tts_url_and_download(word)
            storage.save_tts_file(file_path, content)
        else:
            value = getattr(word, key)
            # 避免清空用户手动填入的内容，比如有些单词没有翻译
            if value:
                note[key] = value
    return mw.col.update_note(note)
