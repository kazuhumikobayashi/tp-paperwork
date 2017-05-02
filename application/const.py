from enum import Enum


FORMULA = [('', ''),
           ('1', '未満切り捨て'),
           ('2', '以下切り捨て'),
           ('3', 'を超える場合切り上げ'),
           ('4', '以上切り上げ'),
           ('5', '単位四捨五入')]

PROJECT_ATTACHMENT_TYPE = {'1': '見積書',
                           '2': '顧客注文書',
                           '3': 'BP注文書',
                           '4': '注文請書',
                           '5': '顧客請求書',
                           '6': 'BP請求書',
                           '9': 'その他'}

BILLING_STATUS = {'1': '請求済み'}

TAX_CLASSIFICATION = [('', ''),
                      ('0', 'なし'),
                      ('8', '8%'),
                      ('10', '10%')]

GENDER = [('男性', '男性'),
          ('女性', '女性')]


class ClientFlag(Enum):
    OUR_COMPANY = 1
    BP = 2
    CLIENT = 3
    END_USER = 4


def get_type_for_select():
    ret = [('', '')]
    type_list = [(key, value) for key, value in sorted(PROJECT_ATTACHMENT_TYPE.items())]
    ret.extend(type_list)
    return ret


def get_billing_status_for_select():
    ret = [('', '')]
    type_list = [(key, value) for key, value in sorted(BILLING_STATUS.items())]
    ret.extend(type_list)
    return ret
