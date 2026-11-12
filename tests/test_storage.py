import os
import tempfile
import unittest

from reposteria import db, storage


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp.name, "test.db")
        db.init_db(self.db_path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_customer_inventory_recipe_cost(self):
        c = storage.add_customer(self.db_path, "Ana", phone="555", email="ana@test.com")
        self.assertEqual(c["name"], "Ana")
        harina = storage.add_inventory_item(self.db_path, "Harina", "kg", cost_per_unit=2.0, quantity=10)
        azucar = storage.add_inventory_item(self.db_path, "Azucar", "kg", cost_per_unit=1.5, quantity=5)
        r = storage.add_recipe(
            self.db_path,
            "Pastel",
            yield_units=2,
            ingredients=[{"item_id": harina["id"], "quantity": 1.0}, {"item_id": azucar["id"], "quantity": 0.5}],
        )
        self.assertEqual(len(r["ingredients"]), 2)
        cost = storage.recipe_cost(self.db_path, r["id"], margin=0.5)
        # total 1*2 + 0.5*1.5 = 2.75, unit 1.375, suggested 2.0625
        self.assertAlmostEqual(cost["total_cost"], 2.75, places=4)
        self.assertAlmostEqual(cost["suggested_unit_price"], 2.0625, places=4)

    def test_order_confirm_deducts_inventory_and_invoice(self):
        c = storage.add_customer(self.db_path, "Luis")
        harina = storage.add_inventory_item(self.db_path, "Harina", "kg", cost_per_unit=2.0, quantity=10)
        r = storage.add_recipe(self.db_path, "Galleta", yield_units=1, ingredients=[{"item_id": harina["id"], "quantity": 2.0}])
        quote = storage.quote_order(self.db_path, [{"recipe_id": r["id"], "quantity": 3}], margin=0.25)
        self.assertEqual(len(quote["items"]), 1)
        self.assertAlmostEqual(quote["items"][0]["unit_price"], 5.0, places=4)  # 4.0 cost * 1.25
        order = storage.create_order(self.db_path, c["id"], [{"recipe_id": r["id"], "quantity": 3}], margin=0.25, confirm=True)
        self.assertEqual(order["status"], "confirmed")
        inv = storage.list_inventory(self.db_path)[0]
        self.assertAlmostEqual(inv["quantity"], 4.0, places=4)  # 10 - 2*3
        invoice = storage.create_invoice(self.db_path, order["id"])
        self.assertEqual(invoice["order_id"], order["id"])
        self.assertAlmostEqual(invoice["total"], order["total"], places=4)
        self.assertEqual(len(invoice["items"]), 1)
        with self.assertRaises(storage.ValidationError):
            storage.create_invoice(self.db_path, order["id"])

    def test_insufficient_inventory(self):
        c = storage.add_customer(self.db_path, "Mia")
        harina = storage.add_inventory_item(self.db_path, "Harina", "kg", cost_per_unit=2.0, quantity=1)
        r = storage.add_recipe(self.db_path, "Pan", yield_units=1, ingredients=[{"item_id": harina["id"], "quantity": 2.0}])
        with self.assertRaises(storage.ValidationError):
            storage.create_order(self.db_path, c["id"], [{"recipe_id": r["id"], "quantity": 1}], confirm=True)


if __name__ == "__main__":
    unittest.main()
