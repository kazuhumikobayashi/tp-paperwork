import unittest

from application.domain.model.immutables.round import Round


class RoundTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Round.down.name, '切り捨て')
        self.assertEqual(Round.off.name, '四捨五入')

    def test_parse(self):
        down = 1
        off = 2

        self.assertEqual(Round.parse(down), Round.down)
        self.assertEqual(Round.parse(off), Round.off)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Round.parse(0))
        self.assertIsNone(Round.parse('a'))

    def test_str(self):
        down = '1'
        off = '2'

        self.assertEqual(str(Round.down), down)
        self.assertEqual(str(Round.off), off)
