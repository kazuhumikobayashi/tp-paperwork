import unittest

from application.domain.model.immutables.status import Status
from tests import BaseTestCase


class StatusTests(unittest.TestCase):

    def test_name(self):
        self.assertEqual(Status.start.name, '01:契約開始')
        self.assertEqual(Status.placed.name, '02:発注完了')
        self.assertEqual(Status.received.name, '03:受注完了')
        self.assertEqual(Status.done.name, '04:契約完了')
        self.assertEqual(Status.failure.name, '99:失注')

    def test_parse(self):
        start = 1
        placed = 2
        received = 3
        done = 4
        failure = 99

        self.assertEqual(Status.parse(start), Status.start)
        self.assertEqual(Status.parse(placed), Status.placed)
        self.assertEqual(Status.parse(received), Status.received)
        self.assertEqual(Status.parse(done), Status.done)
        self.assertEqual(Status.parse(failure), Status.failure)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Status.parse(0))
        self.assertIsNone(Status.parse('a'))

    def test_is_done(self):
        self.assertFalse(Status.start.is_done())
        self.assertFalse(Status.placed.is_done())
        self.assertFalse(Status.received.is_done())
        self.assertTrue(Status.done.is_done())
        self.assertFalse(Status.failure.is_done())
