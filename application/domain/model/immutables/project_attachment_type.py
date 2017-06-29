from enum import Enum


class ProjectAttachmentType(Enum):
    estimate = 1
    client_purchase_order_or_invoice = 2
    bp_purchase_order_or_invoice = 3
    client_order_confirmation_or_invoice = 4
    bp_order_confirmation_or_invoice = 5
    other = 9

    @property
    def name(self):
        if self._value_ == self.estimate.value:
            return '見積書'
        elif self._value_ == self.client_purchase_order_or_invoice.value:
            return '顧客注文書、請書'
        elif self._value_ == self.bp_purchase_order_or_invoice.value:
            return 'BP注文書、請書'
        elif self._value_ == self.client_order_confirmation_or_invoice.value:
            return '顧客請求書、納品書'
        elif self._value_ == self.bp_order_confirmation_or_invoice.value:
            return 'BP請求書、納品書'
        else:
            return 'その他'

    @staticmethod
    def get_type_for_select():
        ret = [('', '')]
        type_list = [(str(attachment_type.value), attachment_type.name) for attachment_type in ProjectAttachmentType]
        ret.extend(type_list)
        return ret

    @staticmethod
    def parse(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                pass
        for attachment_type in ProjectAttachmentType:
            if attachment_type.value == value:
                return attachment_type
        return None

    def __str__(self):
        return str(self._value_)
