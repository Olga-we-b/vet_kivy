from database import (
    create_tables,
    get_owners,
    get_animals,
    get_doctors,
    get_services,
    get_visits,
    save_owner,
    save_animal,
)
from owner import Owner
from animal import Animal


def main():
    create_tables()

    while True:
        print("\n--- Gabinet Fidel&Bajzel ---")
        print("1. Właściciele")
        print("2. Zwierzęta")
        print("3. Lekarze")
        print("4. Usługi")
        print("5. Wizyty")
        print("6. Właściciele")
        print("7. Zwierzęta")
        print("0. Wyjście")

        choice = input("Wybierz opcję: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            rows = get_owners()
        elif choice == "2":
            rows = get_animals()
        elif choice == "3":
            rows = get_doctors()
        elif choice == "4":
            rows = get_services()
        elif choice == "5":
            rows = get_visits()
        elif choice == "6":
            name = input("Imię: ").strip()
            surname = input("Nazwisko: ").strip()
            email = input("Email: ").strip()
            phone = input("Telefon: ").strip()

            if not name or not surname or not phone:
                print("Imię, nazwisko i telefon są wymagane.")
                continue

            owner = Owner(None, name, surname, email, phone)
            save_owner(owner)
            print("Zapisano właściciela, ID:", owner.id)
            continue
        elif choice == "7":
            owners = get_owners()

            if not owners:
                print("Najpierw dodaj właściciela.")
                continue

            for row in owners:
                print(row)

            try:
                owner_id = int(input("ID właściciela: "))
            except ValueError:
                print("ID musi być liczbą.")
                continue

            if owner_id not in [row[0] for row in owners]:
                print("Nie ma właściciela o takim ID.")
                continue

            name = input("Imię zwierzęcia: ").strip()
            kind = input("Gatunek: ").strip()
            breed = input("Rasa: ").strip()
            gender = input("Płeć: ").strip()

            if not name or not kind:
                print("Imię i gatunek są wymagane.")
                continue

            animal = Animal(
                None, name, kind, breed, None, gender, owner_id
            )
            save_animal(animal)
            print("Zapisano zwierzę, ID:", animal.id)
            continue
        else:
            print("Nieprawidłowa opcja.")
            continue

        if not rows:
            print("Brak danych.")
        else:
            for row in rows:
                print(row)


if __name__ == "__main__":
    main()