from application.domain.model.immutables.status import Status
from tests import BaseTestCase


class StatusTests(BaseTestCase):

    def setUp(self):
        super(StatusTests, self).setUp()

    def tearDown(self):
        super(StatusTests, self).tearDown()

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

        self.assertEquals(Status.parse(start), Status.start)
        self.assertEquals(Status.parse(placed), Status.placed)
        self.assertEquals(Status.parse(received), Status.received)
        self.assertEquals(Status.parse(done), Status.done)
        self.assertEquals(Status.parse(failure), Status.failure)

    def test_parse_fail_is_none(self):
        self.assertIsNone(Status.parse(0))
        self.assertIsNone(Status.parse('a'))
