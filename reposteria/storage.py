from .db import connect, init_db


class ReposteriaError(Exception):
    pass


class NotFound(ReposteriaError):
    pass


class ValidationError(ReposteriaError):
    pass


def _row(conn, table, row_id):
    r = conn.execute(f"SELECT * FROM {table} WHERE id = ?", (row_id,)).fetchone()
    if not r:
        raise NotFound(f"{table} {row_id} no encontrado")
    return dict(r)


# Customers
def add_customer(db_path, name, phone=None, email=None):
    if not name or not str(name).strip():
        raise ValidationError("nombre de cliente requerido")
    conn = connect(db_path)
    try:
        cur = conn.execute(
            "INSERT INTO customers(name, phone, email) VALUES(?,?,?)",
            (name.strip(), phone, email),
        )
        conn.commit()
        return _row(conn, "customers", cur.lastrowid)
    finally:
        conn.close()


def list_customers(db_path):
    conn = connect(db_path)
    try:
        rows = conn.execute("SELECT * FROM customers ORDER BY id").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# Inventory
def add_inventory_item(db_path, name, unit, cost_per_unit=0.0, quantity=0.0):
    if not name or not str(name).strip():
        raise ValidationError("nombre de insumo requerido")
    if not unit or not str(unit).strip():
        raise ValidationError("unidad requerida")
    conn = connect(db_path)
    try:
        cur = conn.execute(
            "INSERT INTO inventory_items(name, unit, cost_per_unit, quantity) VALUES(?,?,?,?)",
            (name.strip(), unit.strip(), float(cost_per_unit), float(quantity)),
        )
        conn.commit()
        return _row(conn, "inventory_items", cur.lastrowid)
    finally:
        conn.close()


def list_inventory(db_path):
    conn = connect(db_path)
    try:
        rows = conn.execute("SELECT * FROM inventory_items ORDER BY id").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def adjust_inventory(db_path, item_id, delta_quantity):
    conn = connect(db_path)
    try:
        item = _row(conn, "inventory_items", item_id)
        new_q = float(item["quantity"]) + float(delta_quantity)
        if new_q < 0:
            raise ValidationError("inventario insuficiente")
        conn.execute("UPDATE inventory_items SET quantity=? WHERE id=?", (new_q, item_id))
        conn.commit()
        return _row(conn, "inventory_items", item_id)
    finally:
        conn.close()


# Recipes
def add_recipe(db_path, name, yield_units=1, ingredients=None, notes=None):
    if not name or not str(name).strip():
        raise ValidationError("nombre de receta requerido")
    if int(yield_units) <= 0:
        raise ValidationError("yield_units debe ser > 0")
    ingredients = ingredients or []
    conn = connect(db_path)
    try:
        cur = conn.execute(
            "INSERT INTO recipes(name, yield_units, notes) VALUES(?,?,?)",
            (name.strip(), int(yield_units), notes),
        )
        rid = cur.lastrowid
        for ing in ingredients:
            item_id = int(ing["item_id"])
            qty = float(ing["quantity"])
            if qty <= 0:
                raise ValidationError("cantidad de ingrediente debe ser > 0")
            _row(conn, "inventory_items", item_id)
            conn.execute(
                "INSERT INTO recipe_ingredients(recipe_id,item_id,quantity) VALUES(?,?,?)",
                (rid, item_id, qty),
            )
        conn.commit()
        return get_recipe(db_path, rid)
    finally:
        conn.close()


def get_recipe(db_path, recipe_id):
    conn = connect(db_path)
    try:
        r = conn.execute("SELECT * FROM recipes WHERE id=?", (recipe_id,)).fetchone()
        if not r:
            raise NotFound(f"recipe {recipe_id} no encontrada")
        ings = conn.execute(
            """SELECT ri.item_id, ri.quantity, ii.name, ii.unit, ii.cost_per_unit
               FROM recipe_ingredients ri JOIN inventory_items ii ON ii.id=ri.item_id
               WHERE ri.recipe_id=? ORDER BY ii.name""",
            (recipe_id,),
        ).fetchall()
        data = dict(r)
        data["ingredients"] = [dict(x) for x in ings]
        return data
    finally:
        conn.close()


def list_recipes(db_path):
    conn = connect(db_path)
    try:
        rows = conn.execute("SELECT * FROM recipes ORDER BY id").fetchall()
        return [get_recipe(db_path, r["id"]) for r in rows]
    finally:
        conn.close()


def recipe_cost(db_path, recipe_id, margin=0.3):
    recipe = get_recipe(db_path, recipe_id)
    total_cost = 0.0
    for ing in recipe["ingredients"]:
        total_cost += float(ing["quantity"]) * float(ing["cost_per_unit"])
    unit_cost = total_cost / max(int(recipe["yield_units"]), 1)
    suggested_unit_price = unit_cost * (1.0 + float(margin))
    return {
        "recipe_id": recipe_id,
        "name": recipe["name"],
        "yield_units": recipe["yield_units"],
        "total_cost": round(total_cost, 4),
        "unit_cost": round(unit_cost, 4),
        "margin": float(margin),
        "suggested_unit_price": round(suggested_unit_price, 4),
    }


# Orders
def create_order(db_path, customer_id, items, notes=None, margin=0.3, confirm=False):
    if not items:
        raise ValidationError("pedido requiere items")
    conn = connect(db_path)
    try:
        _row(conn, "customers", customer_id)
        # compute items and check inventory if confirming
        computed = []
        total = 0.0
        for it in items:
            rid = int(it["recipe_id"])
            qty = int(it["quantity"])
            if qty <= 0:
                raise ValidationError("cantidad de item debe ser > 0")
            recipe = get_recipe(db_path, rid)
            cost_info = recipe_cost(db_path, rid, margin=margin)
            unit_price = float(it.get("unit_price", cost_info["suggested_unit_price"]))
            subtotal = round(unit_price * qty, 4)
            total += subtotal
            computed.append({"recipe": recipe, "quantity": qty, "unit_price": unit_price, "subtotal": subtotal})
        if confirm:
            # verify and deduct inventory
            needed = {}
            for c in computed:
                for ing in c["recipe"]["ingredients"]:
                    needed[ing["item_id"]] = needed.get(ing["item_id"], 0.0) + float(ing["quantity"]) * c["quantity"]
            for item_id, need in needed.items():
                inv = conn.execute("SELECT quantity FROM inventory_items WHERE id=?", (item_id,)).fetchone()
                if not inv or float(inv["quantity"]) < need:
                    raise ValidationError(f"inventario insuficiente para item {item_id}")
            for item_id, need in needed.items():
                conn.execute("UPDATE inventory_items SET quantity = quantity - ? WHERE id=?", (need, item_id))
        status = "confirmed" if confirm else "draft"
        cur = conn.execute(
            "INSERT INTO orders(customer_id,status,notes,total) VALUES(?,?,?,?)",
            (customer_id, status, notes, round(total, 4)),
        )
        oid = cur.lastrowid
        for c in computed:
            conn.execute(
                "INSERT INTO order_items(order_id,recipe_id,quantity,unit_price,subtotal) VALUES(?,?,?,?,?)",
                (oid, c["recipe"]["id"], c["quantity"], c["unit_price"], c["subtotal"]),
            )
        conn.commit()
        return get_order(db_path, oid)
    finally:
        conn.close()


def get_order(db_path, order_id):
    conn = connect(db_path)
    try:
        o = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
        if not o:
            raise NotFound(f"order {order_id} no encontrado")
        items = conn.execute(
            """SELECT oi.*, r.name as recipe_name FROM order_items oi
               JOIN recipes r ON r.id=oi.recipe_id WHERE oi.order_id=?""",
            (order_id,),
        ).fetchall()
        data = dict(o)
        data["items"] = [dict(i) for i in items]
        return data
    finally:
        conn.close()


def list_orders(db_path):
    conn = connect(db_path)
    try:
        rows = conn.execute("SELECT * FROM orders ORDER BY id").fetchall()
        return [get_order(db_path, r["id"]) for r in rows]
    finally:
        conn.close()


def quote_order(db_path, items, margin=0.3):
    if not items:
        raise ValidationError("cotización requiere items")
    # use recipe_cost for pricing without persisting
    init_db(db_path)
    lines = []
    total = 0.0
    for it in items:
        rid = int(it["recipe_id"])
        qty = int(it["quantity"])
        cost_info = recipe_cost(db_path, rid, margin=margin)
        unit_price = float(it.get("unit_price", cost_info["suggested_unit_price"]))
        subtotal = round(unit_price * qty, 4)
        total += subtotal
        lines.append({"recipe_id": rid, "name": cost_info["name"], "quantity": qty, "unit_price": unit_price, "subtotal": subtotal})
    return {"items": lines, "total": round(total, 4), "margin": margin}


# Invoices
def create_invoice(db_path, order_id):
    conn = connect(db_path)
    try:
        order = get_order(db_path, order_id)
        existing = conn.execute("SELECT id FROM invoices WHERE order_id=?", (order_id,)).fetchone()
        if existing:
            raise ValidationError("ya existe factura para este pedido")
        cur = conn.execute(
            "INSERT INTO invoices(order_id,customer_id,total,status) VALUES(?,?,?,?)",
            (order_id, order["customer_id"], order["total"], "issued"),
        )
        inv_id = cur.lastrowid
        for it in order["items"]:
            desc = f"{it['recipe_name']} x{it['quantity']}"
            conn.execute(
                "INSERT INTO invoice_items(invoice_id,description,quantity,unit_price,subtotal) VALUES(?,?,?,?,?)",
                (inv_id, desc, it["quantity"], it["unit_price"], it["subtotal"]),
            )
        conn.commit()
        return get_invoice(db_path, inv_id)
    finally:
        conn.close()


def get_invoice(db_path, invoice_id):
    conn = connect(db_path)
    try:
        inv = conn.execute("SELECT * FROM invoices WHERE id=?", (invoice_id,)).fetchone()
        if not inv:
            raise NotFound(f"invoice {invoice_id} no encontrada")
        items = conn.execute("SELECT * FROM invoice_items WHERE invoice_id=?", (invoice_id,)).fetchall()
        data = dict(inv)
        data["items"] = [dict(i) for i in items]
        return data
    finally:
        conn.close()


def list_invoices(db_path):
    conn = connect(db_path)
    try:
        rows = conn.execute("SELECT * FROM invoices ORDER BY id").fetchall()
        out = []
        for r in rows:
            inv = dict(r)
            items = conn.execute("SELECT * FROM invoice_items WHERE invoice_id=?", (r["id"],)).fetchall()
            inv["items"] = [dict(i) for i in items]
            out.append(inv)
        return out
    finally:
        conn.close()
