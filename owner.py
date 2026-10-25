
class Owner:
    def __init__(self, id, name, surname, email, phone_number):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.phone_number = phone_number

    def update_data(self, name, surname, email, phone_number):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone_number = phone_number