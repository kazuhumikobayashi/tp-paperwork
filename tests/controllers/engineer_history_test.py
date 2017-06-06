from datetime import date, datetime

from nose.tools import ok_

from application import db
from application.domain.model.engineer_history import EngineerHistory
from application.domain.model.immutables.rule import Rule
from application.domain.repository.engineer_history_repository import EngineerHistoryRepository
from tests import BaseTestCase


class EngineerHistoryTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(EngineerHistoryTests, cls).setUpClass()

    def setUp(self):
        super(EngineerHistoryTests, self).setUp()
        self.engineer_history_repository = EngineerHistoryRepository()

    def tearDown(self):
        super(EngineerHistoryTests, self).tearDown()

    # 技術者履歴登録画面に遷移する。
    def test_get_engineer_history_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/engineer_history/create?engineer_id=1')
        self.assertEqual(result.status_code, 200)

    # 技術者履歴を登録する。
    def test_create_engineer_history(self):
        before = len(self.engineer_history_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        engineer_id = 2

        result = self.app.post('/engineer_history/create?engineer_id=' + str(engineer_id), data={
            'engineer_id': engineer_id,
            'payment_start_day': date(2017, 1, 1).strftime('%Y/%m'),
            'payment_end_day': date(2017, 2, 28).strftime('%Y/%m'),
            'payment_per_month': '100000',
            'payment_rule': str(Rule.fixed),
            'payment_fraction_calculation1': '',
            'payment_fraction_calculation2': ''
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.engineer_history_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

        # 追加したデータを削除
        engineer_history = self.engineer_history_repository.find_by_id(
            len(self.engineer_history_repository.find_all()) - 1)
        result = self.app.get(
            '/engineer_history/delete/' + str(engineer_history.id))
        # 削除できたことを確認
        self.assertEqual(result.status_code, 302)

    # 技術者履歴画面に遷移する。
    def test_get_engineer_history(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        engineer_history = self.engineer_history_repository.find_all()[0]

        result = self.app.get('/engineer_history/' + str(engineer_history.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない技術者履歴の場合はnot_found
    def test_get_engineer_history_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/engineer_history/0')
        self.assertEqual(result.status_code, 404)

    # 技術者履歴を保存できる
    def test_save_engineer_history(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        engineer_history = self.engineer_history_repository.find_all()[0]

        expected = 200000
        engineer_history_id = engineer_history.id

        result = self.app.post('/engineer_history/' + str(engineer_history.id), data={
            'payment_per_month': expected
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/engineer_history/' + str(engineer_history.id) in result.headers['Location'])

        engineer_history_after_save = self.engineer_history_repository.find_by_id(
            engineer_history_id)
        actual = engineer_history_after_save.payment_per_month
        self.assertEqual(actual, expected)

    # 技術者履歴を削除できる
    def test_delete_engineer_history(self):
        # 削除用のエンジニアを登録
        engineer_history = EngineerHistory(
            engineer_id=1,
            payment_start_day=date(2017, 1, 1),
            payment_end_day=date(2017, 2, 28),
            payment_per_month=100000,
            payment_rule=Rule.fixed,
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(engineer_history)
        db.session.commit()

        delete_engineer_history_id = engineer_history.id
        engineer_id = engineer_history.engineer_id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        engineer_history = self.engineer_history_repository.find_by_id(
            delete_engineer_history_id)

        result = self.app.get(
            '/engineer_history/delete/' + str(engineer_history.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/engineer/detail/' + str(engineer_id)
            in result.headers['Location'])

        # 削除した履歴が存在しないことを確認
        engineer_history = self.engineer_history_repository.find_by_id(
            delete_engineer_history_id)
        self.assertIsNone(engineer_history.id)

    # 存在しない履歴は削除できない
    def test_delete_engineer_fail(self):
        before = len(self.engineer_history_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/engineer_history/delete/0')
        self.assertEqual(result.status_code, 302)
        ok_('/engineer' in result.headers['Location'])

        after = len(self.engineer_history_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 支払い契約開始年月は、前回の支払い終了年月より前の年月で登録できない。
    def test_validation_payment_start_day1(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        engineer_id = 3

        # 以下のデータを新規作成。
        result = self.app.post('/engineer_history/create?engineer_id=' + str(engineer_id), data={
            'engineer_id': engineer_id,
            'payment_start_day': date(2017, 1, 1).strftime('%Y/%m'),
            'payment_end_day': date(2017, 5, 31).strftime('%Y/%m'),
            'payment_per_month': '100000',
            'payment_rule': str(Rule.fixed),
            'payment_fraction_calculation1': '',
            'payment_fraction_calculation2': ''
        })
        self.assertEqual(result.status_code, 302)

        # engineer=3に紐づく履歴が1件であることを確認
        before = len(
            self.engineer_history_repository.find_by_engineer_id(engineer_id))
        self.assertEqual(before, 1)
        # 登録した履歴を取得
        before_engineer_history = self.engineer_history_repository.find_by_engineer_id(
            engineer_id)[0]
        before_payment_start_day = before_engineer_history.payment_start_day

        # 前回の支払い終了年月が2017年5月のため、開始年月をその前の年月で登録できないことを確認する。
        result = self.app.post('/engineer_history/' + str(before_engineer_history.id), data={
            'payment_start_day': date(2017, 3, 1).strftime('%Y/%m'),
            'payment_end_day': before_engineer_history.payment_end_day,
            'payment_per_month': before_engineer_history.payment_per_month,
            'payment_rule': before_engineer_history.payment_rule,
            'payment_fraction_calculation1': '',
            'payment_fraction_calculation2': ''
        })
        self.assertEqual(result.status_code, 200)

        # engineer=4に紐づく履歴が1件であることを確認（履歴が切られていないことを確認）
        after = len(
            self.engineer_history_repository.find_by_engineer_id(engineer_id))
        self.assertEqual(after, 1)
        # もう一度登録した履歴を取得する
        after_engineer_history = self.engineer_history_repository.find_by_engineer_id(
            engineer_id)[0]
        after_payment_start_day = after_engineer_history.payment_start_day

        # 更新前と更新後の契約開始年月に変化がないことを確認。
        self.assertEqual(before_payment_start_day, after_payment_start_day)

        # 追加したデータを削除
        result = self.app.get('/engineer_history/delete/' +
                              str(after_engineer_history.id))
        # 削除できたことを確認
        self.assertEqual(result.status_code, 302)

    # 支払い契約開始年月＜支払い契約終了年月　の関係にあることを確認。
    def test_validation_payment_start_day2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        engineer_id = 4

        # 以下のデータを新規作成。
        result = self.app.post('/engineer_history/create?engineer_id=' + str(engineer_id), data={
            'payment_start_day': date(2017, 1, 1).strftime('%Y/%m'),
            'payment_end_day': date(2017, 5, 31).strftime('%Y/%m'),
            'payment_per_month': '100000',
            'payment_rule': str(Rule.fixed),
            'payment_fraction_calculation1': '',
            'payment_fraction_calculation2': ''
        })
        self.assertEqual(result.status_code, 302)

        # engineer=4に紐づく履歴が1件であることを確認
        before = len(
            self.engineer_history_repository.find_by_engineer_id(engineer_id))
        self.assertEqual(before, 1)
        # 登録した履歴を取得
        before_engineer_history = self.engineer_history_repository.find_by_engineer_id(
            engineer_id)[0]
        before_payment_start_day = before_engineer_history.payment_start_day

        # 支払い終了年月が2017年8月のため、開始年月を2017年10月月で登録できないことを確認する。
        result = self.app.post('/engineer_history/' + str(before_engineer_history.id), data={
            'payment_start_day': date(2017, 10, 1).strftime('%Y/%m'),
            'payment_end_day': date(2017, 8, 1).strftime('%Y/%m'),
            'payment_per_month': before_engineer_history.payment_per_month,
            'payment_rule': before_engineer_history.payment_rule,
            'payment_fraction_calculation1': '',
            'payment_fraction_calculation2': ''
        })
        self.assertEqual(result.status_code, 200)

        # engineer=4に紐づく履歴が1件であることを確認（履歴が切られていないことを確認）
        after = len(
            self.engineer_history_repository.find_by_engineer_id(engineer_id))
        self.assertEqual(after, 1)
        # もう一度登録した履歴を取得する
        after_engineer_history = self.engineer_history_repository.find_by_engineer_id(
            engineer_id)[0]
        after_payment_start_day = after_engineer_history.payment_start_day

        # 更新前と更新後の契約開始年月に変化がないことを確認。
        self.assertEqual(before_payment_start_day, after_payment_start_day)

        # 追加したデータを削除
        result = self.app.get('/engineer_history/delete/' +
                              str(after_engineer_history.id))
        # 削除できたことを確認
        self.assertEqual(result.status_code, 302)

    # 支払いのルールが変動の場合、validationチェックが働くことを確認
    def test_required_if_variable(self):
        before = len(self.engineer_history_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        engineer_id = 5

        result = self.app.post('/engineer_history/create?engineer_id=' + str(engineer_id), data={
            'payment_start_day': date(2017, 1, 1).strftime('%Y/%m'),
            'payment_end_day': date(2017, 2, 28).strftime('%Y/%m'),
            'payment_per_month': '100000',
            'payment_rule': str(Rule.variable),
            'payment_fraction_calculation1': '',
            'payment_fraction_calculation2': ''
        })
        self.assertEqual(result.status_code, 200)

        after = len(self.engineer_history_repository.find_all())
        # 全体の件数に変化がないことを確認
        self.assertEqual(before, after)

    # 支払いフリー時間が入力されているとき、支払い上限時間と下限時間のヴァリデーションをスルー
    def test_through_free_hour_validation(self):
        before = len(self.engineer_history_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        engineer_id = 5

        # 上限・下限時間を登録しなくてもデータが追加されることを確認する。
        result = self.app.post('/engineer_history/create?engineer_id=' + str(engineer_id), data={
            'payment_start_day': date(2017, 1, 1).strftime('%Y/%m'),
            'payment_end_day': date(2017, 2, 28).strftime('%Y/%m'),
            'payment_per_month': '100000',
            'payment_rule': str(Rule.variable),
            # 'payment_bottom_base_hour': 1,
            # 'payment_top_base_hour': 2,
            'payment_free_base_hour': '8h×100',
            'payment_per_hour': '1/100, 1/150',
            'payment_per_bottom_hour': 3,
            'payment_per_top_hour': 4,
            'payment_fraction': 100,
            'payment_fraction_calculation1': 1,
            'payment_fraction_calculation2': 1,
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.engineer_history_repository.find_all())
        # 全体の件数が1件増えていることを確認。
        self.assertEqual(before + 1, after)

        # 追加したデータを削除
        engineer_history = self.engineer_history_repository.find_by_id(
            len(self.engineer_history_repository.find_all()) - 1)
        result = self.app.get(
            '/engineer_history/delete/' + str(engineer_history.id))
        # 削除できたことを確認
        self.assertEqual(result.status_code, 302)

    # 支払い上限時間か下限時間が入力されているとき、支払いフリー時間のヴァリデーションをスルー
    def test_through_bottom_and_top_hour_validation(self):
        before = len(self.engineer_history_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        engineer_id = 5

        # フリー時間を登録しなくてもデータが追加されることを確認する。
        result = self.app.post('/engineer_history/create?engineer_id=' + str(engineer_id), data={
            'payment_start_day': date(2017, 1, 1).strftime('%Y/%m'),
            'payment_end_day': date(2017, 2, 28).strftime('%Y/%m'),
            'payment_per_month': '100000',
            'payment_rule': str(Rule.variable),
            'payment_bottom_base_hour': 1,
            'payment_top_base_hour': 2,
            # 'payment_free_base_hour': '',
            'payment_per_hour': '1/100, 1/150',
            'payment_per_bottom_hour': 3,
            'payment_per_top_hour': 4,
            'payment_fraction': 100,
            'payment_fraction_calculation1': 1,
            'payment_fraction_calculation2': 1,
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.engineer_history_repository.find_all())
        # 全体の件数が1件増えていることを確認。
        self.assertEqual(before + 1, after)

        # 追加したデータを削除
        engineer_history = self.engineer_history_repository.find_by_id(
            len(self.engineer_history_repository.find_all()) - 1)
        result = self.app.get(
            '/engineer_history/delete/' + str(engineer_history.id))
        # 削除できたことを確認
        self.assertEqual(result.status_code, 302)
