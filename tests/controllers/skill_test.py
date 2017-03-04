from datetime import datetime

from nose.tools import ok_

from application import db
from application.domain.model.skill import Skill
from application.domain.repository.skill_repository import SkillRepository
from tests import BaseTestCase


class SkillTests(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(SkillTests, cls).setUpClass()
        cls().create_skills()

    def setUp(self):
        super(SkillTests, self).setUp()
        self.skill_repository = SkillRepository()

    def tearDown(self):
        super(SkillTests, self).tearDown()

    # スキルの検索画面に遷移する。
    def test_get_skill(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/skill/')
        self.assertEqual(result.status_code, 200)

    # ２ページ目に遷移する。
    def test_skill_page2(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/skill/page/2')
        self.assertEqual(result.status_code, 200)

    # スキルを検索する。
    def test_search_skill(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/skill/?skill_name=test')
        self.assertEqual(result.status_code, 200)

    # スキル登録画面に遷移する。
    def test_get_skill_create(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/skill/create')
        self.assertEqual(result.status_code, 200)

    # スキル登録する。
    def test_create_skill(self):
        before = len(self.skill_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.post('/skill/create', data={
            'skill_name': 'テスト登録'
        })
        self.assertEqual(result.status_code, 302)

        after = len(self.skill_repository.find_all())
        # 1件追加されていることを確認
        self.assertEqual(before + 1, after)

    # スキル登録に失敗する。
    def test_create_skill_fail(self):
        before = len(self.skill_repository.find_all())
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        # 同じ名称のスキルは登録できない
        result = self.app.post('/skill/create', data={
            'skill_name': 'test0'
        })
        self.assertEqual(result.status_code, 200)

        after = len(self.skill_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    # スキル詳細画面に遷移する。
    def test_get_skill_detail(self):
        # ログインする
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        skill = self.skill_repository.find_all()[0]

        result = self.app.get('/skill/detail/' + str(skill.id))
        self.assertEqual(result.status_code, 200)

    # 存在しないスキルの場合はnot_found
    def test_get_skill_detail_fail(self):
        # ログインする
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/skill/detail/0')
        self.assertEqual(result.status_code, 404)

    # スキルを保存できる
    def test_save_skill(self):
        shain_number = 'test1'
        self.app.post('/login', data={
            'shain_number': shain_number,
            'password': 'test'
        })
        skill = self.skill_repository.find_all()[0]

        expected = '単体テスト_変更'
        skill_id = skill.id

        result = self.app.post('/skill/detail/' + str(skill_id), data={
            'skill_name': expected
        })
        # 保存できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/skill/detail/' + str(skill.id) in result.headers['Location'])

        skill = self.skill_repository.find_by_id(skill_id)
        actual = skill.skill_name
        self.assertEqual(actual, expected)

    # スキルを削除できる
    def test_delete_skill(self):
        # 削除用のスキルを登録
        skill = Skill(
            skill_name='削除用スキル',
            created_at=datetime.today(),
            created_user='test',
            updated_at=datetime.today(),
            updated_user='test')
        db.session.add(skill)
        db.session.commit()

        delete_skill_id = skill.id

        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })
        skill = self.skill_repository.find_by_id(delete_skill_id)

        result = self.app.get('/skill/delete/' + str(skill.id))
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/skill' in result.headers['Location'])

        # 削除したスキルが存在しないことを確認
        skill = self.skill_repository.find_by_id(delete_skill_id)
        self.assertIsNone(skill.id)

    # 存在しないスキルは削除できない
    def test_delete_skill_fail(self):
        before = len(self.skill_repository.find_all())
        # ログイン
        self.app.post('/login', data={
            'shain_number': 'test1',
            'password': 'test'
        })

        result = self.app.get('/skill/delete/0')
        # 削除できることを確認
        self.assertEqual(result.status_code, 302)
        ok_('/skill' in result.headers['Location'])

        after = len(self.skill_repository.find_all())
        # 前後で件数が変わっていないことを確認
        self.assertEqual(before, after)

    def create_skills(self):
        for num in range(12):
            skill = Skill(
                skill_name='test' + str(num),
                created_at=datetime.today(),
                created_user='test',
                updated_at=datetime.today(),
                updated_user='test')
            db.session.add(skill)
        db.session.commit()
