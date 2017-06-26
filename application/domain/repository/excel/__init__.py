import os
from datetime import datetime

from flask import session, send_file
from openpyxl import Workbook, load_workbook


class Excel(object):

    def __init__(self, template_file=None):
        if template_file:
            # テンプレートファイルの読み込み
            self.workbook = load_workbook("excel/templates/" + template_file)
        else:
            # 新規ファイルの作成
            self.workbook = Workbook()
        directory = datetime.today().strftime("%Y%m%d")
        path = "excel/temporary/" + directory
        hms = datetime.today().strftime("%H%M%S") + "%03d" % (datetime.now().microsecond // 1000)
        temp_file_name = hms + "temp" + "_" + str(session['user']['id'])
        if not os.path.isdir(path):
            os.makedirs(path)
        self.file_name = template_file
        self.file_path = path + "/" + temp_file_name

    def save(self, file_name=None):
        if file_name:
            self.file_name = file_name
        self.workbook.save(self.file_path)

    def download(self):
        return send_file("../" + self.file_path,
                         mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         attachment_filename=self.file_name, as_attachment=True)

    @property
    def active(self):
        return self.workbook.active

    @active.setter
    def active(self, value):
        self.workbook.active = value
