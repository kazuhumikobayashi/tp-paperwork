from openpyxl.styles import Alignment, Font


class AddressSheet(object):

    def __init__(self, report):
        self.report = report

    # 宛名シート作成
    def create_address_sheet(self):
        self.report.excel.workbook.create_sheet(title='宛名')
        ws = self.report.excel.workbook['宛名']
        address = ws['B1']

        # 宛名を記入する位置を修正
        ws.column_dimensions['A'].width = 5

        # 宛名の枠の大きさを修正
        ws.column_dimensions['B'].width = 30
        ws.row_dimensions[1].height = 110

        # 宛名に値を代入。
        address.value = self.report.get_print_name()

        # 書式修正
        address.font = Font(name='ＭＳ ゴシック')
        address.alignment = Alignment(vertical="distributed" ,wrap_text=True)

        # 余白の調整
        ws.page_margins.top = 0.5
