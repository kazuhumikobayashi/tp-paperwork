from datetime import date, datetime

from nose.tools import ok_

from application import db
from application.domain.model.assigned_members import AssignedMember
from application.domain.repository.assigned_member_repository import AssignedMemberRepository
from tests import BaseTestCase


class AssignedMemberTests(BaseTestCase):

    def setUp(self):
        super(AssignedMemberTests, self).setUp()
        self.assigned_member_repository = AssignedMemberRepository()

    def tearDown(self):
        super(AssignedMemberTests, self).tearDown()

    # 技術者登録画面に遷移する。
    def test_get_assigned_member_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/assigned_member/add')
        self.assertEqual(result.status_code, 200)

    # 技術者を登録する。
    def test_add_assigned_member(self):
        before = len(self.assigned_member_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/assigned_member/add?project_id=1', data={
            'project_id': '1',
            'engineer_id': '1',
            'sales_unit_price': '10',
            'payment_unit_price': '10',
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': '2099/12/31',
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.assigned_member_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

    # 技術者登録に失敗する。
    def test_save_calculation_fail(self):
        before = len(self.assigned_member_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 存在しないassigned_member_idでは登録できない
        result = self.app.post('/assigned_member/detail/99', data={
            'project_id': '1',
            'engineer_id': '1',
            'sales_unit_price': '10',
            'payment_unit_price': '10',
            'start_date': date.today().strftime('%Y/%m/%d'),
            'end_date': '2099/12/31',
        })
        self.assertEqual(result.status_code, 404)

        after = len(self.assigned_member_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 技術者を削除できる
    def test_delete_assigned_member(self):
        # 削除用の技術者を登録
        assigned_member = AssignedMember(
            project_id=1,
            seq_no=1,
            engineer_id=1,
            sales_unit_price=1,
            payment_unit_price=1,
            start_date=date.today().strftime('%Y/%m/%d'),
            end_date='2099/12/31',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(assigned_member)
        db.session.commit()

        delete_assigned_member_id = assigned_member.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        assigned_member = self.assigned_member_repository.find_by_id(delete_assigned_member_id)

        result = self.app.get('/assigned_member/delete/' + str(assigned_member.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/project/detail/' + str(assigned_member.project_id) in result.headers['Location'])

        # 削除した技術者が存在しないことを確認
        assigned_member = self.assigned_member_repository.find_by_id(delete_assigned_member_id)
        self.assertIsNone(assigned_member.id)

    # 存在しない技術者は削除できない
    def test_delete_assigned_member_fail(self):
        before = len(self.assigned_member_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/assigned_member/delete/0')
        # 削除できないことを確認
        self.assertEqual(result.status_code, 404)

        after = len(self.assigned_member_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)
