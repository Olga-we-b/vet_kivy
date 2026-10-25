class Animal:
    def __init__(self, id, name, kind, breed, date_of_birth, gender, owner_id):
        self.id = id
        self.name = name
        self.kind = kind
        self.breed = breed
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.owner_id = owner_id
    def update_data(self, name, kind, breed, date_of_birth, gender, owner_id):
        self.name = name
        self.kind = kind
        self.breed = breed
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.owner_id = owner_id

