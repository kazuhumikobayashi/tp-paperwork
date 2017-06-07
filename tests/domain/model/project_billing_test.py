from application.domain.model.project_billing import ProjectBilling
from tests import BaseTestCase


class ProjectBillingTests(BaseTestCase):

    def setUp(self):
        super(ProjectBillingTests, self).setUp()

    def tearDown(self):
        super(ProjectBillingTests, self).tearDown()

    def test___repr__(self):
        project_billing = ProjectBilling(
            project_detail_id=1,
            billing_month='2017/1/1',
            billing_content='billing_content',
            billing_amount='billing_amount',
            billing_confirmation_money=10000,
            remarks='remarks',
            created_at=None,
            created_user=None,
            updated_at=None,
            updated_user=None)

        expected = "<ProjectBilling:" + \
                   "'id='{}".format(project_billing.id) + \
                   "', project_detail_id='{}".format(project_billing.project_detail_id) + \
                   "', billing_month='{}".format(project_billing.billing_month) + \
                   "', billing_content='{}".format(project_billing.billing_content) + \
                   "', billing_amount='{}".format(project_billing.billing_amount) + \
                   "', billing_confirmation_money='{}".format(project_billing.billing_confirmation_money) + \
                   "', remarks='{}".format(project_billing.remarks) + \
                   "', created_at='{}".format(project_billing.created_at) + \
                   "', created_user='{}".format(project_billing.created_user) + \
                   "', updated_at='{}".format(project_billing.updated_at) + \
                   "', updated_user='{}".format(project_billing.updated_user) + \
                   "'>"
        actual = str(project_billing)
        self.assertEqual(actual, expected)
