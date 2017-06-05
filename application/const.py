from enum import Enum

RECEIPT_RULE = [('1', '固定'),
                ('2', '変動')]


class ReceiptRule(Enum):
    FIXED = '1'
    VARIABLE = '2'
