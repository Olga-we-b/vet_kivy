from visit_position import VisitPosition
class Visit:
    def __init__(self, id, animal_id, doctor_id, datetime):
        self.id = id
        self.animal_id = animal_id
        self.doctor_id = doctor_id
        self.datetime = datetime
        self.status = "zaplanowana"
        self.diagnosis = ""
        self.recomendation = ""
        self.positions = []

    def cancel(self):
        if self.status != "zaplanowana":
            raise ValueError("Można odwołać tylko zaplanowaną wizytę")
        self.status = "anulowana"

    def finish(self, diagnosis, recommendations):
        if self.status != "zaplanowana":
            raise ValueError("Można zakończyć tylko zaplanowaną wizytę.")
        self.diagnosis = diagnosis
        self.recommendations = recommendations
        self.status = "zakonczona"

    def add_service(self, service):
        if self.status != "zaplanowana":
            raise ValueError("można dodawać pozycje tylko do zaplanowanej wizyty")
        position = VisitPosition(None, self.id, service.id, service.price)

        self.positions.append(position)

    def calculate_cost(self):
        total = 0
        for position in self.positions:
            total += position.price
        return total