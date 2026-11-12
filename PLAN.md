# PLAN — Sistema para Repostería (Laravel + Filament)

## Objetivo
Sistema completo para gestionar una repostería: recetas con ingredientes y rendimiento, costeo y cotización, clientes, pedidos con descuento de inventario, facturación. Interfaz de administración con Filament.

## Stack
- **PHP 8.3 + Laravel 11**
- **Filament 3** (panel de administración)
- **SQLite** (base de datos ligera, autocontenida)
- **PHPUnit** (pruebas unitarias)

## Unidades de trabajo
1. [x] Scaffold Laravel + Filament + SQLite
2. [x] Migraciones: customers, inventory_items, recipes, recipe_ingredients, orders, order_items, invoices, invoice_items
3. [x] Modelos Eloquent con relaciones y lógica de negocio (costo de receta, confirmación de pedido con descuento de inventario, total de factura)
4. [x] Recursos Filament CRUD para Customers, InventoryItems, Recipes, Orders, Invoices
5. [x] Pruebas unitarias (12 tests: Customer, InventoryItem, Recipe, Order, Invoice)
6. [ ] Commit + Push + Pull Request
7. [ ] Registro en SQLite del sistema agente

## Criterios de aceptación
- Migraciones creadas y ejecutadas correctamente
- Modelos con relaciones correctas y lógica de negocio (calculateCost, confirmInventory, calculateTotal)
- Recursos Filament funcionales para cada entidad
- 12 pruebas unitarias pasando (exit code 0)
- Sin TODO/FIXME/stubs
- Commit semántico + PR creado (si hay remoto)

## Comando de tests
```bash
php artisan test
```
