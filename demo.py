from owner import Owner
from animal import Animal
from service import Service
from datetime import datetime
from doctor import Doctor
from visit import Visit
from database import create_tables, get_animals
from database import save_owner
from database import get_owners
from database import save_animal
from database import get_owners
from database import save_doctor, get_doctors

service = Service(1, "Szczepienie", 10000)
print(service.name, service.price)

service.change_price(12000)
print(service.name, service.price)

owner = Owner(1, "Olga", "Apiecionek", "olga@example.com", "123456789")

animal = Animal(1, "Fidel", "kot", "europejski", None, "samiec", owner.id)
print(animal.name, animal.owner_id)

animal.update_data("Fidel", "kot", "europejski", None, "samiec", owner.id)
print(animal.kind, animal.gender)


doctor = Doctor(1, "Anna", "Kowalska", "12345")
visit = Visit(1, animal.id, doctor.id, datetime(2026, 10, 23, 10, 0))

service.change_price(10000)
visit.add_service(service)

service.change_price(12000)
print("Koszt wizyty:", visit.calculate_cost() / 100, "zł")

visit.finish("Zwierzę zdrowe", "Kontrola za rok")
print("Status:", visit.status)
print("Rozpoznanie:", visit.diagnosis)

visit2 = Visit(2, animal.id, doctor.id, datetime(2026, 10, 23, 11, 0))
visit2.cancel()
print(visit2.status)

try:
    visit2.finish("Zwierzę zdrowe", "Kontrola za rok")
except ValueError as error:
    print(error)

create_tables()


"""
new_owner = Owner(
    None, "Anna", "Nowak", "anna@example.com", "123456789"
)
save_owner(new_owner)
print("Zapisano właściciela, ID:", new_owner.id)

"""


for row in get_owners():
    print(row)
"""
owners = get_owners()
owner_id = owners[0][0]

new_animal = Animal(
    None, "Bajzel", "kot", "europejski", None, "samiec", owner_id
)
save_animal(new_animal)
print("Zapisano zwierzę, ID:", new_animal.id)
"""
for row in get_animals():
    print(row)

doctor = Doctor("2", "Anna", "Kowalska", "12345")
save_doctor(doctor)
for row in get_doctors():
    print(row)