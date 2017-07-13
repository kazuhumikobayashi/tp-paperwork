import unittest

from application.domain.model.immutables.message import Message


class MessageTests(unittest.TestCase):

    def test_str(self):
        saved = '保存しました。'
        saving_failed = '保存できませんでした。入力内容を確認してください。'
        deleted = '削除しました。'

        self.assertEqual(str(Message.saved), saved)
        self.assertEqual(str(Message.saving_failed), saving_failed)
        self.assertEqual(str(Message.deleted), deleted)
