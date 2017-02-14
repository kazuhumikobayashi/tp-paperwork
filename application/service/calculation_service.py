from application.domain.repository.calculation_repository import CalculationRepository


class CalculationService(object):
    repository = CalculationRepository()

    def find(self, page, calculation_name):
        if calculation_name == '' or None:
            return self.find_all(page)
        return self.repository.find(page, calculation_name)

    def find_all(self, page=None):
        return self.repository.find_all(page)

    def find_all_for_select(self):
        ret = [('', '')]
        calculation_list = [(str(h.id), h.calculation_name) for h in self.find_all()]
        ret.extend(calculation_list)
        return ret

    def find_by_id(self, calculation_id):
        return self.repository.find_by_id(calculation_id)

    def save(self, calculation):
        return self.repository.save(calculation)

    def destroy(self, calculation):
        return self.repository.destroy(calculation)
