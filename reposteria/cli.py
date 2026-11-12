import argparse
import json
import sys
from pathlib import Path
from . import storage, db


def default_db():
    return str(Path(__file__).resolve().parents[1] / "reposteria.db")


def jprint(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_init(args):
    db.init_db(args.db)
    print(f"DB inicializada en {args.db}")


def cmd_customer_add(args):
    db.init_db(args.db)
    c = storage.add_customer(args.db, args.name, phone=args.phone, email=args.email)
    jprint(c)


def cmd_customer_list(args):
    db.init_db(args.db)
    jprint(storage.list_customers(args.db))


def cmd_inventory_add(args):
    db.init_db(args.db)
    it = storage.add_inventory_item(args.db, args.name, args.unit, args.cost, args.quantity)
    jprint(it)


def cmd_inventory_list(args):
    db.init_db(args.db)
    jprint(storage.list_inventory(args.db))


def cmd_inventory_adjust(args):
    db.init_db(args.db)
    it = storage.adjust_inventory(args.db, args.id, args.delta)
    jprint(it)


def parse_ingredients(text):
    # format: item_id:qty,item_id:qty
    if not text:
        return []
    out = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise ValueError("ingrediente debe ser item_id:qty")
        a, b = part.split(":", 1)
        out.append({"item_id": int(a), "quantity": float(b)})
    return out


def cmd_recipe_add(args):
    db.init_db(args.db)
    ings = parse_ingredients(args.ingredients)
    r = storage.add_recipe(args.db, args.name, yield_units=args.yield_units, ingredients=ings, notes=args.notes)
    jprint(r)


def cmd_recipe_list(args):
    db.init_db(args.db)
    jprint(storage.list_recipes(args.db))


def cmd_recipe_cost(args):
    db.init_db(args.db)
    jprint(storage.recipe_cost(args.db, args.id, margin=args.margin))


def parse_order_items(text):
    # format: recipe_id:qty[:unit_price]
    if not text:
        return []
    out = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        bits = part.split(":")
        if len(bits) < 2:
            raise ValueError("item debe ser recipe_id:qty[:unit_price]")
        item = {"recipe_id": int(bits[0]), "quantity": int(bits[1])}
        if len(bits) >= 3 and bits[2] != "":
            item["unit_price"] = float(bits[2])
        out.append(item)
    return out


def cmd_order_quote(args):
    db.init_db(args.db)
    items = parse_order_items(args.items)
    jprint(storage.quote_order(args.db, items, margin=args.margin))


def cmd_order_create(args):
    db.init_db(args.db)
    items = parse_order_items(args.items)
    o = storage.create_order(args.db, args.customer_id, items, notes=args.notes, margin=args.margin, confirm=args.confirm)
    jprint(o)


def cmd_order_list(args):
    db.init_db(args.db)
    jprint(storage.list_orders(args.db))


def cmd_order_show(args):
    db.init_db(args.db)
    jprint(storage.get_order(args.db, args.id))


def cmd_invoice_create(args):
    db.init_db(args.db)
    inv = storage.create_invoice(args.db, args.order_id)
    jprint(inv)


def cmd_invoice_show(args):
    db.init_db(args.db)
    jprint(storage.get_invoice(args.db, args.id))


def cmd_invoice_list(args):
    db.init_db(args.db)
    jprint(storage.list_invoices(args.db))


def build_parser():
    p = argparse.ArgumentParser(prog="reposteria", description="Sistema de gestión para repostería")
    p.add_argument("--db", default=default_db(), help="Ruta a la base SQLite")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init-db")
    sp.set_defaults(func=cmd_init)

    c = sub.add_parser("customer")
    cs = c.add_subparsers(dest="subcmd", required=True)
    a = cs.add_parser("add")
    a.add_argument("--name", required=True)
    a.add_argument("--phone")
    a.add_argument("--email")
    a.set_defaults(func=cmd_customer_add)
    l = cs.add_parser("list")
    l.set_defaults(func=cmd_customer_list)

    inv = sub.add_parser("inventory")
    ins = inv.add_subparsers(dest="subcmd", required=True)
    a = ins.add_parser("add")
    a.add_argument("--name", required=True)
    a.add_argument("--unit", required=True)
    a.add_argument("--cost", type=float, default=0.0)
    a.add_argument("--quantity", type=float, default=0.0)
    a.set_defaults(func=cmd_inventory_add)
    l = ins.add_parser("list")
    l.set_defaults(func=cmd_inventory_list)
    adj = ins.add_parser("adjust")
    adj.add_argument("--id", type=int, required=True)
    adj.add_argument("--delta", type=float, required=True)
    adj.set_defaults(func=cmd_inventory_adjust)

    r = sub.add_parser("recipe")
    rs = r.add_subparsers(dest="subcmd", required=True)
    a = rs.add_parser("add")
    a.add_argument("--name", required=True)
    a.add_argument("--yield-units", type=int, default=1)
    a.add_argument("--ingredients", default="", help="item_id:qty,item_id:qty")
    a.add_argument("--notes")
    a.set_defaults(func=cmd_recipe_add)
    l = rs.add_parser("list")
    l.set_defaults(func=cmd_recipe_list)
    cost = rs.add_parser("cost")
    cost.add_argument("--id", type=int, required=True)
    cost.add_argument("--margin", type=float, default=0.3)
    cost.set_defaults(func=cmd_recipe_cost)

    o = sub.add_parser("order")
    osub = o.add_subparsers(dest="subcmd", required=True)
    q = osub.add_parser("quote")
    q.add_argument("--items", required=True, help="recipe_id:qty[:unit_price],...")
    q.add_argument("--margin", type=float, default=0.3)
    q.set_defaults(func=cmd_order_quote)
    cr = osub.add_parser("create")
    cr.add_argument("--customer-id", type=int, required=True)
    cr.add_argument("--items", required=True)
    cr.add_argument("--notes")
    cr.add_argument("--margin", type=float, default=0.3)
    cr.add_argument("--confirm", action="store_true")
    cr.set_defaults(func=cmd_order_create)
    l = osub.add_parser("list")
    l.set_defaults(func=cmd_order_list)
    sh = osub.add_parser("show")
    sh.add_argument("--id", type=int, required=True)
    sh.set_defaults(func=cmd_order_show)

    invc = sub.add_parser("invoice")
    isub = invc.add_subparsers(dest="subcmd", required=True)
    cr = isub.add_parser("create")
    cr.add_argument("--order-id", type=int, required=True)
    cr.set_defaults(func=cmd_invoice_create)
    sh = isub.add_parser("show")
    sh.add_argument("--id", type=int, required=True)
    sh.set_defaults(func=cmd_invoice_show)
    l = isub.add_parser("list")
    l.set_defaults(func=cmd_invoice_list)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except storage.ReposteriaError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
