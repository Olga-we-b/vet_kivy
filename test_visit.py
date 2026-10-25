import unittest
from datetime import datetime

from visit import Visit
from service import Service


class TestVisit(unittest.TestCase):
    def setUp(self):
        self.visit = Visit(
            1, 1, 1, datetime(2026, 10, 24, 10, 0)
        )

    def test_cost_and_historical_price(self):
        service = Service(1, "Szczepienie", 10000)
        self.visit.add_service(service)
        self.visit.add_service(Service(2, "Konsultacja", 5000))

        service.change_price(12000)

        self.assertEqual(self.visit.calculate_cost(), 15000)

    def test_finish_visit(self):
        self.visit.finish("Zwierzę zdrowe", "Kontrola za rok")

        self.assertEqual(self.visit.status, "zakonczona")
        self.assertEqual(self.visit.diagnosis, "Zwierzę zdrowe")
        self.assertEqual(
            self.visit.recommendations, "Kontrola za rok"
        )

    def test_cancel_blocks_finishing(self):
        self.visit.cancel()

        self.assertEqual(self.visit.status, "anulowana")

        with self.assertRaises(ValueError):
            self.visit.finish("Zwierzę zdrowe", "Kontrola")


if __name__ == "__main__":
    unittest.main()