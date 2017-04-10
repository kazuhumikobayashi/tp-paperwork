from datetime import datetime

from nose.tools import ok_

from application import db
from application.domain.model.business_category import BusinessCategory
from application.domain.repository.business_category_repository import BusinessCategoryRepository
from tests import BaseTestCase


class BusinessCategoryTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(BusinessCategoryTests, cls).setUpClass()

    def setUp(self):
        super(BusinessCategoryTests, self).setUp()
        self.business_category_repository = BusinessCategoryRepository()

    def tearDown(self):
        super(BusinessCategoryTests, self).tearDown()

    # 業種の検索画面に遷移する。
    def test_get_business_category(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/business_category/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_business_category_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/business_category/page/2')
        self.assertEqual(result.status_code, 200)

    # 業種を検索する。
    def test_search_business_category(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/business_category/?business_category_name=test')
        self.assertEqual(result.status_code, 200)

    # 業種登録画面に遷移する。
    def test_get_business_category_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/business_category/create')
        self.assertEqual(result.status_code, 200)

    # 業種登録する。
    def test_create_business_category(self):
        before = len(self.business_category_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/business_category/create', data={
            'business_category_name': 'テスト登録'
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.business_category_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

    # 業種登録に失敗する。
    def test_create_business_category_fail(self):
        before = len(self.business_category_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 同じ名称の業種は登録できない
        result = self.app.post('/business_category/create', data={
            'business_category_name': 'test0'
        })
        self.assertEqual(result.status_code, 200)

        after = len(self.business_category_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # 業種詳細画面に遷移する。
    def test_get_business_category_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        business_category = self.business_category_repository.find_all()[0]

        result = self.app.get('/business_category/detail/' + str(business_category.id))
        self.assertEqual(result.status_code, 200)

    # 存在しない業種の場合はnot_found
    def test_get_business_category_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/business_category/detail/0')
        self.assertEqual(result.status_code, 404)

    # 業種を保存できる
    def test_save_business_category(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        business_category = self.business_category_repository.find_all()[0]

        expected = '単体テスト_変更'
        business_category_id = business_category.id

        result = self.app.post('/business_category/detail/' + str(business_category_id), data={
            'business_category_name': expected
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/business_category/detail/' + str(business_category.id) in result.headers['Location'])

        business_category = self.business_category_repository.find_by_id(business_category_id)
        actual = business_category.business_category_name
        self.assertEqual(actual, expected)

    # 業種を削除できる
    def test_delete_business_category(self):
        # 削除用の業種を登録
        business_category = BusinessCategory(
            business_category_name='削除用業種',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(business_category)
        db.session.commit()

        delete_business_category_id = business_category.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        business_category = self.business_category_repository.find_by_id(delete_business_category_id)

        result = self.app.get('/business_category/delete/' + str(business_category.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/business_category' in result.headers['Location'])

        # 削除した業種が存在しないことを確認
        business_category = self.business_category_repository.find_by_id(delete_business_category_id)
        self.assertIsNone(business_category.id)

    # 存在しない業種は削除できない
    def test_delete_business_category_fail(self):
        before = len(self.business_category_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/business_category/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/business_category' in result.headers['Location'])

        after = len(self.business_category_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)
