from datetime import datetime

from openpyxl.styles import Border, Side, Font

from application.domain.model.immutables.billing_timing import BillingTiming
from application.domain.repository.engineer_history_repository import EngineerHistoryRepository
from application.domain.repository.excel import Excel

engineer_history_repository = EngineerHistoryRepository()


class ClientOrderReport(object):

    def __init__(self, project):
        self.project = project
        self.excel = Excel("client_order.xlsx")
        self.ws = self.excel.active

    def download(self):
        self._create_excel()

        return self.excel.download()

    def _create_excel(self):
        self.write_client_order().write_style()

        # エクセルを一時フォルダに保存
        self.excel.save('04_注文請書（{}）_{}.xlsx'.format(
                                                       self.project.client_order_no or "",
                                                       datetime.today().strftime("%Y%m%d")))

    def write_client_order(self):
        # 値を代入
        self.ws.get_named_range("printed_date")[0].value = datetime.today().date()
        if self.project.client_company:
            self.ws.get_named_range("client_company_name")[0].value = self.project.client_company.company_name
        self.ws.get_named_range("client_order_no")[0].value = self.project.client_order_no
        self.ws.get_named_range("estimation_no")[0].value = self.project.estimation_no
        self.ws.get_named_range("project_name")[0].value = self.project.project_name
        if self.project.contract_form:
            self.ws.get_named_range("contract_form")[0].value = self.project.contract_form.name
        self.ws.get_named_range("estimated_total_amount")[0].value = self.project.estimated_total_amount or 0
        self.ws.get_named_range("contents")[0].value = self.project.contents
        self.ws.get_named_range("start_date")[0].value = self.project.start_date
        self.ws.get_named_range("end_date")[0].value = self.project.end_date
        self.ws.get_named_range("responsible_person")[0].value = self.project.responsible_person
        self.ws.get_named_range("quality_control")[0].value = self.project.quality_control
        self.ws.get_named_range("subcontractor")[0].value = self.project.subcontractor
        self.ws.get_named_range("working_place")[0].value = self.project.working_place
        self.ws.get_named_range("delivery_place")[0].value = self.project.delivery_place
        self.ws.get_named_range("deliverables")[0].value = self.project.deliverables
        if self.project.billing_timing == BillingTiming.billing_by_month:
            self.ws.get_named_range("inspection_date")[0].value = '毎月月末'
        else:
            self.ws.get_named_range("inspection_date")[0].value = self.project.inspection_date
        if self.project.billing_timing:
            self.ws.get_named_range("billing_timing")[0].value = self.project.billing_timing.name_for_report
        self.ws.get_named_range("remarks")[0].value = self.remarks()
        return self

    def write_style(self):
        # フォント設定
        self.ws.get_named_range("client_company_name")[0].font = Font(name="ＭＳ ゴシック", size=14, underline="single")
        # 表示形式
        self.ws.get_named_range("printed_date")[0].number_format = 'yyyy年m月d日'
        self.ws.get_named_range("start_date")[0].number_format = 'yyyy年m月d日'
        self.ws.get_named_range("end_date")[0].number_format = 'yyyy年m月d日'
        # 罫線
        self.write_border_to_merged_cell(row=14)
        self.write_border_to_merged_cell(row=16)
        self.write_border_to_cell(row=18)
        self.write_border_to_cell(row=19)
        self.write_border_to_cell(row=20)
        self.write_border_to_merged_cell(row=21)
        self.write_border_to_cell(row=23)
        self.write_border_to_cell(row=24)
        self.write_border_to_cell(row=25)
        self.write_border_to_cell(row=26)
        self.write_border_to_cell(row=27)
        self.write_border_to_cell(row=28)
        self.write_border_to_cell(row=29)
        self.write_border_to_cell(row=30)
        self.write_border_to_merged_cell(row=31)
        self.ws['B32'].border = Border(left=Side(style='thin'), right=Side(style='thin'), bottom=Side(style='thin'))

    # セル結合されていない1行の項目に罫線を引く
    def write_border_to_cell(self, row):
        for column_num in ['D', 'E', 'F', 'G']:
            self.ws[column_num + str(row)].border = Border(bottom=Side(style='thin'))
        self.ws['H' + str(row)].border = Border(bottom=Side(style='thin'), right=Side(style='thin'))

    # セルが結合されて2行になっている項目に罫線を引く
    def write_border_to_merged_cell(self, row):
        self.ws['H' + str(row)].border = Border(top=Side(style='thin'), right=Side(style='thin'))
        for column_num in ['D', 'E', 'F', 'G']:
            self.ws[column_num + str(row + 1)].border = Border(bottom=Side(style='thin'))
        self.ws['H' + str(row + 1)].border = Border(bottom=Side(style='thin'), right=Side(style='thin'))

    def remarks(self):
        text = '上記以外の条件は当社見積書(見積書No.{})の通りとします。'\
            .format(self.project.estimation_no or "               ")
        return text
