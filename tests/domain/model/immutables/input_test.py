import unittest

from application.domain.model.immutables.input_flag import InputFlag


class InputFlagTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(InputFlag.yet.name, '未')
        self.assertEqual(InputFlag.done.name, '済')

    def test_parse(self):
        yet = 0
        done = 1

        self.assertEquals(InputFlag.parse(yet), InputFlag.yet)
        self.assertEquals(InputFlag.parse(done), InputFlag.done)

    def test_parse_fail_is_none(self):
        self.assertIsNone(InputFlag.parse(10))
        self.assertIsNone(InputFlag.parse('a'))

    def test_str(self):
        yet = '0'
        done = '1'

        self.assertEqual(str(InputFlag.yet), yet)
        self.assertEqual(str(InputFlag.done), done)
