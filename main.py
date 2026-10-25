from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from database import create_tables, get_owners, get_animals, get_doctors, get_services
import sqlite3
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from owner import Owner
from database import save_owner
from kivy.uix.spinner import Spinner
from animal import Animal
from database import save_animal
from pathlib import Path
from kivy.clock import Clock
from kivy.uix.image import Image

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(15)
        )

        logo_path = Path(__file__).resolve().parent / "logo.png"
        layout.add_widget(Image(source=str(logo_path)))

        layout.add_widget(Label(
            text="Fidel&Bajzel",
            font_size="32sp",
            size_hint_y=None,
            height=dp(60)
        ))

        layout.add_widget(Label(
            text="Gabinet weterynaryjny",
            font_size="18sp",
            size_hint_y=None,
            height=dp(40)
        ))

        self.add_widget(layout)

    def on_enter(self, *args):
        Clock.schedule_once(self.open_home, 2.5)

    def open_home(self, dt):
        self.manager.current = "home"



class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical", padding=20, spacing=10
        )
        layout.add_widget(Label(text="Gabinet Fidel&Bajzel"))

        button = Button(text="Właściciele")
        button.bind(on_release=self.open_owners)
        layout.add_widget(button)

        button2 = Button(text="Zwierzęta")
        button2.bind(on_release=self.open_animals)
        layout.add_widget(button2)

        doctor_button = Button(text="Lekarze")
        doctor_button.bind(on_release=self.open_doctors)
        layout.add_widget(doctor_button)

        service_button = Button(text="Usługi")
        service_button.bind(on_release=self.open_services)
        layout.add_widget(service_button)

        self.add_widget(layout)

    def open_owners(self, button):
        self.manager.current = "owners"

    def open_animals(self, button):
        self.manager.current = "animals"

    def open_doctors(self, button):
        self.manager.current = "doctors"

    def open_services(self, button):
        self.manager.current = "services"

class OwnersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical", padding=20, spacing=10
        )

        layout.add_widget(Label(
            text="Właściciele",
            size_hint_y=None,
            height=dp(50)
        ))

        scroll = ScrollView()

        self.owner_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8)
        )
        self.owner_list.bind(
            minimum_height=self.owner_list.setter("height")
        )

        scroll.add_widget(self.owner_list)
        layout.add_widget(scroll)

        add_button = Button(
            text="Dodaj właściciela",
            size_hint_y=None,
            height=dp(50)
        )
        add_button.bind(on_release=self.open_add_form)
        layout.add_widget(add_button)

        button = Button(
            text="Powrót", size_hint_y=None, height=dp(50)
        )
        button.bind(on_release=self.go_back)
        layout.add_widget(button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.owner_list.clear_widgets()
        owners = get_owners()

        if not owners:
            self.owner_list.add_widget(Label(
                text="Brak właścicieli.",
                size_hint_y=None,
                height=dp(50)
            ))

        for owner in owners:
            self.owner_list.add_widget(Label(
                text=f"{owner[0]}. {owner[1]} {owner[2]}\n"
                     f"Telefon: {owner[4]}",
                size_hint_y=None,
                height=dp(70)
            ))

    def go_back(self, button):
        self.manager.current = "home"

    def open_add_form(self, button):
        form = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        name = TextInput(hint_text="Imię", multiline=False)
        surname = TextInput(hint_text="Nazwisko", multiline=False)
        email = TextInput(hint_text="Email (opcjonalnie)", multiline=False)
        phone = TextInput(hint_text="Telefon", multiline=False)

        for field in (name, surname, email, phone):
            form.add_widget(field)

        message = Label(text="")
        form.add_widget(message)

        buttons = BoxLayout(
            spacing=dp(8), size_hint_y=None, height=dp(50)
        )
        save_button = Button(text="Zapisz")
        cancel_button = Button(text="Anuluj")
        buttons.add_widget(save_button)
        buttons.add_widget(cancel_button)
        form.add_widget(buttons)

        popup = Popup(
            title="Nowy właściciel",
            content=form,
            size_hint=(0.95, 0.9),
            auto_dismiss=False
        )

        def save(button):
            owner_name = name.text.strip()
            owner_surname = surname.text.strip()
            owner_email = email.text.strip()
            owner_phone = phone.text.strip()

            if not owner_name or not owner_surname or not owner_phone:
                message.text = "Podaj imię, nazwisko i telefon."
                return

            if owner_email:
                parts = owner_email.split("@")
                if (
                        len(parts) != 2
                        or not parts[0]
                        or "." not in parts[1]
                        or parts[1].startswith(".")
                        or parts[1].endswith(".")
                        or any(char.isspace() for char in owner_email)
                ):
                    message.text = "Podaj poprawny email."
                    return

            owner = Owner(
                None, owner_name, owner_surname,
                owner_email, owner_phone
            )

            try:
                save_owner(owner)
            except sqlite3.Error:
                message.text = "Nie udało się zapisać danych."
                return

            popup.dismiss()
            self.on_pre_enter()

        save_button.bind(on_release=save)
        cancel_button.bind(on_release=popup.dismiss)
        popup.open()


class AnimalsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical", padding=20, spacing=10
        )

        layout.add_widget(Label(
            text="Zwierzęta",
            size_hint_y=None,
            height=dp(50)
        ))

        scroll = ScrollView()

        self.animal_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8)
        )
        self.animal_list.bind(
            minimum_height=self.animal_list.setter("height")
        )

        scroll.add_widget(self.animal_list)
        layout.add_widget(scroll)

        add_button = Button(
            text="Dodaj zwierzę",
            size_hint_y=None,
            height=dp(50)
        )
        add_button.bind(on_release=self.open_add_form)
        layout.add_widget(add_button)

        button = Button(
            text="Powrót", size_hint_y=None, height=dp(50)
        )
        button.bind(on_release=self.go_back)
        layout.add_widget(button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.animal_list.clear_widgets()
        animals = get_animals()

        if not animals:
            self.animal_list.add_widget(Label(
                text="Lista pusta",
                size_hint_y=None,
                height=dp(50)
            ))

        for animal in animals:
            birth_date = animal[4] or "Nieznana"

            self.animal_list.add_widget(Label(
                text=f"{animal[0]}. {animal[1]} — {animal[2]}\n"
                     f"Rasa: {animal[3]}\n"
                     f"Data urodzenia: {birth_date}\n"
                     f"Płeć: {animal[5]} | ID właściciela: {animal[6]}",
                size_hint_y=None,
                height=dp(110)
            ))

    def open_add_form(self, button):
        form = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        name = TextInput(hint_text="Imię", multiline=False)
        kind = TextInput(hint_text="Gatunek", multiline=False)
        breed = TextInput(hint_text="Rasa (opcjonalnie)", multiline=False)
        gender = TextInput(hint_text="Płeć (opcjonalnie)", multiline=False)

        owners = get_owners()
        owner_options = {
            f"{row[0]}. {row[1]} {row[2]}": row[0]
            for row in owners
        }

        owner_spinner = Spinner(
            text="Wybierz właściciela",
            values=list(owner_options)
        )

        for field in (name, kind, breed, gender, owner_spinner):
            form.add_widget(field)

        message = Label(
            text="" if owners else "Najpierw dodaj właściciela."
        )
        form.add_widget(message)

        buttons = BoxLayout(
            spacing=dp(8), size_hint_y=None, height=dp(50)
        )
        save_button = Button(text="Zapisz", disabled=not owners)
        cancel_button = Button(text="Anuluj")
        buttons.add_widget(save_button)
        buttons.add_widget(cancel_button)
        form.add_widget(buttons)

        popup = Popup(
            title="Nowe zwierzę",
            content=form,
            size_hint=(0.95, 0.9),
            auto_dismiss=False
        )

        def save(button):
            animal_name = name.text.strip()
            animal_kind = kind.text.strip()

            if not animal_name or not animal_kind:
                message.text = "Podaj imię i gatunek."
                return

            owner_id = owner_options.get(owner_spinner.text)

            if owner_id is None:
                message.text = "Wybierz właściciela."
                return

            animal = Animal(
                None,
                animal_name,
                animal_kind,
                breed.text.strip(),
                None,
                gender.text.strip(),
                owner_id
            )

            try:
                save_animal(animal)
            except sqlite3.Error:
                message.text = "Nie udało się zapisać danych."
                return

            popup.dismiss()
            self.on_pre_enter()

        save_button.bind(on_release=save)
        cancel_button.bind(on_release=popup.dismiss)
        popup.open()
    def go_back(self, button):
        self.manager.current = "home"

class DoctorsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical", padding=20, spacing=10
        )
        layout.add_widget(Label(
            text="Lekarze", size_hint_y=None, height=dp(50)
        ))

        scroll = ScrollView()
        self.doctor_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8)
        )
        self.doctor_list.bind(
            minimum_height=self.doctor_list.setter("height")
        )
        scroll.add_widget(self.doctor_list)
        layout.add_widget(scroll)

        button = Button(
            text="Powrót", size_hint_y=None, height=dp(50)
        )
        button.bind(on_release=self.go_back)
        layout.add_widget(button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.doctor_list.clear_widgets()
        doctors = get_doctors()

        if not doctors:
            self.doctor_list.add_widget(Label(
                text="Brak lekarzy.",
                size_hint_y=None,
                height=dp(50)
            ))

        for doctor in doctors:
            self.doctor_list.add_widget(Label(
                text=f"{doctor[0]}. {doctor[1]} {doctor[2]}\n"
                     f"Numer PWZ: {doctor[3]}",
                size_hint_y=None,
                height=dp(70)
            ))

    def go_back(self, button):
        self.manager.current = "home"


class ServicesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical", padding=20, spacing=10
        )
        layout.add_widget(Label(
            text="Usługi", size_hint_y=None, height=dp(50)
        ))

        scroll = ScrollView()
        self.service_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8)
        )
        self.service_list.bind(
            minimum_height=self.service_list.setter("height")
        )
        scroll.add_widget(self.service_list)
        layout.add_widget(scroll)

        button = Button(
            text="Powrót", size_hint_y=None, height=dp(50)
        )
        button.bind(on_release=self.go_back)
        layout.add_widget(button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        self.service_list.clear_widgets()
        services = get_services()

        if not services:
            self.service_list.add_widget(Label(
                text="Brak usług.",
                size_hint_y=None,
                height=dp(50)
            ))

        for service in services:
            price = (
                f"{service[2] // 100},"
                f"{service[2] % 100:02d} zł"
            )
            self.service_list.add_widget(Label(
                text=f"{service[0]}. {service[1]}\nCena: {price}",
                size_hint_y=None,
                height=dp(70)
            ))

    def go_back(self, button):
        self.manager.current = "home"


class FidelBajzelApp(App):
    def build(self):
        create_tables()

        manager = ScreenManager()
        manager.add_widget(SplashScreen(name="splash"))
        manager.add_widget(HomeScreen(name="home"))
        manager.add_widget(OwnersScreen(name="owners"))
        manager.add_widget(AnimalsScreen(name="animals"))
        manager.add_widget(DoctorsScreen(name="doctors"))
        manager.add_widget(ServicesScreen(name="services"))


        return manager


if __name__ == "__main__":
    FidelBajzelApp().run()