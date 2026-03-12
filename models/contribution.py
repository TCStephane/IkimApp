class Contribution:
    def __init__(self, member_id, cycle_id, amount, date):
        self.member_id = member_id
        self.cycle_id = cycle_id
        self.amount = amount
        self.date = date

    def save(self):
        pass

    @staticmethod
    def get_by_member(member_id):
        pass

    @staticmethod
    def get_all():
        pass
