from enum import Enum


class Message(Enum):
    saved = '保存しました。'
    saving_failed = '保存できませんでした。入力内容を確認してください。'
    deleted = '削除しました。'

    def __str__(self):
        return str(self._value_)
