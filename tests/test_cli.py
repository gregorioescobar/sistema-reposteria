import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

from reposteria.cli import main


def run_cli(args, db_path):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(["--db", db_path] + args)
    out = buf.getvalue().strip()
    return code, out


class CLITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp.name, "cli.db")

    def tearDown(self):
        self.tmp.cleanup()

    def test_full_flow_cli(self):
        code, _ = run_cli(["init-db"], self.db_path)
        self.assertEqual(code, 0)
        code, out = run_cli(["customer", "add", "--name", "Ana"], self.db_path)
        self.assertEqual(code, 0)
        cust = json.loads(out)
        code, out = run_cli(["inventory", "add", "--name", "Harina", "--unit", "kg", "--cost", "2", "--quantity", "10"], self.db_path)
        item = json.loads(out)
        code, out = run_cli(["recipe", "add", "--name", "Pastel", "--yield-units", "2", "--ingredients", f"{item['id']}:1"], self.db_path)
        self.assertEqual(code, 0)
        recipe = json.loads(out)
        code, out = run_cli(["recipe", "cost", "--id", str(recipe['id']), "--margin", "0.5"], self.db_path)
        self.assertEqual(code, 0)
        cost = json.loads(out)
        self.assertAlmostEqual(cost["unit_cost"], 1.0, places=4)
        code, out = run_cli(["order", "create", "--customer-id", str(cust['id']), "--items", f"{recipe['id']}:2", "--confirm"], self.db_path)
        self.assertEqual(code, 0)
        order = json.loads(out)
        self.assertEqual(order["status"], "confirmed")
        code, out = run_cli(["invoice", "create", "--order-id", str(order['id'])], self.db_path)
        self.assertEqual(code, 0)
        inv = json.loads(out)
        self.assertEqual(inv["order_id"], order['id'])
        code, out = run_cli(["invoice", "show", "--id", str(inv['id'])], self.db_path)
        self.assertEqual(code, 0)
        shown = json.loads(out)
        self.assertEqual(len(shown["items"]), 1)


if __name__ == "__main__":
    unittest.main()
