import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database
from owner import Owner
from animal import Animal


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.db_path = Path(self.temp_dir.name) / "test.db"

        self.patcher = patch(
            "database.get_connection",
            side_effect=self.get_test_connection
        )
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        database.create_tables()

    def get_test_connection(self):
        connection = sqlite3.connect(str(self.db_path))
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def test_owner_is_saved(self):
        owner = Owner(
            None, "Anna", "Nowak", "anna@example.com", "123456789"
        )
        database.save_owner(owner)

        rows = database.get_owners()

        self.assertEqual(len(rows), 1)
        self.assertEqual(
            rows[0],
            (
                owner.id, "Anna", "Nowak",
                "anna@example.com", "123456789"
            )
        )

    def test_animal_requires_existing_owner(self):
        animal = Animal(
            None, "Fidel", "kot", "europejski",
            None, "samiec", 999
        )

        with self.assertRaises(sqlite3.IntegrityError):
            database.save_animal(animal)

        self.assertEqual(database.get_animals(), [])


if __name__ == "__main__":
    unittest.main()