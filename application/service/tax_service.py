from application.domain.repository.tax_repository import TaxRepository


class TaxService(object):
    repository = TaxRepository()

    def find(self, page, tax_rate):
        if tax_rate == '' or None:
            return self.find_all(page)
        return self.repository.find(page, tax_rate)

    def find_all(self, page):
        return self.repository.find_all(page)

    def find_by_id(self, tax_id):
        return self.repository.find_by_id(tax_id)

    def save(self, tax):
        return self.repository.save(tax)

    def destroy(self, tax):
        return self.repository.destroy(tax)
