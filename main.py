# This Python file uses the following encoding: utf-8
import os

from core import storage
from core.mojidict_server import MojiServer

TTS_DIR_PATH = '/Users/qiyu/Library/ApplicationSupport/Anki2/qiyu/collection.media'


def download_all():
    server = MojiServer()
    server.login('qiyu.one@gmail.com', '11301127')

    words = []
    for r in server.fetch_all_from_server():
        file_path = os.path.join(TTS_DIR_PATH, 'moji_' + r.target_id + '.mp3')
        if not os.path.lexists(file_path):
            tts_url = server.get_tts_url(r)
            storage.save_tts_file(file_path, tts_url)
        if r.accent is None:
            r.accent = ''
        words.append(r)
    with open('/Users/qiyu/Downloads/moji.txt', 'w') as f:
        f.write('\n'.join(
            [format_row(r)
             for r in
             words]))


def format_row(r):
    try:
        return '\t'.join([r.target_id, str(r.target_type),
                          r.title, r.spell, r.accent, r.pron, r.excerpt,
                          f'[sound:moji_{r.target_id}.mp3]',
                          f'<a href="https://www.mojidict.com/details/{r.target_id}">Moji Web</a>'])
    except Exception:
        print("处理异常", r.spell)
        raise


if __name__ == "__main__":
    download_all()
