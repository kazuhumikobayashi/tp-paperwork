from datetime import datetime

from application.domain.repository.excel import Excel
from application.service.report.sheet.payment_list_by_department_sheet import PaymentListByDepartmentSheet
from application.service.report.sheet.payment_list_order_by_payment_date_sheet import PaymentListByPaymentDateSheet


class PaymentListReport(object):

    def __init__(self, payment_lists_by_department, project_list_order_by_payment_date, month):
        self.payment_lists_by_department = payment_lists_by_department
        self.project_list_order_by_payment_date = project_list_order_by_payment_date
        self.month = month
        self.excel = Excel("payment_list.xlsx")

    def download(self):
        self._create_excel()

        return self.excel.download()

    def _create_excel(self):

        # 部署ごとの支払い一覧を作成
        self.excel.workbook['委託費'].title = '委託費{}月'.format(self.month.month)
        payment_list_by_department_sheet = PaymentListByDepartmentSheet(
            payment_lists_by_department=self.payment_lists_by_department,
            month=self.month,
            ws=self.excel.workbook['委託費{}月'.format(self.month.month)]
        )
        payment_list_by_department_sheet.write_payment_list_by_department()

        # 支払日ごとの支払い一覧を作成
        self.excel.workbook['支払日別'].title = '支払日別{}月'.format(self.month.month)
        payment_list_order_by_payment_date = PaymentListByPaymentDateSheet(
            payment_list_order_by_payment_date=self.project_list_order_by_payment_date,
            month=self.month,
            ws=self.excel.workbook['支払日別{}月'.format(self.month.month)]
        )
        payment_list_order_by_payment_date.write_payment_list_order_by_payment_date()

        # エクセルを一時フォルダに保存
        self.excel.save('支払一覧_{}.xlsx'.format(datetime.today().strftime("%Y%m%d")))
