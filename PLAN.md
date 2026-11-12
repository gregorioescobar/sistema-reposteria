# PLAN — Sistema para Repostería

## Objetivo
Sistema ligero y autocontenido para gestionar una repostería: recetas (con ingredientes y rendimiento), costeo y cotización, clientes, pedidos, inventario de insumos y facturación. Persistencia en SQLite y CLI probada.

## Stack elegido (ligero, autocontenido)
- **Python 3 (stdlib)** + **SQLite3**: sin dependencias externas ni servicios.
- **argparse** para CLI; **unittest** para pruebas.
- Nota: la idea original proponía PHP/Laravel/Filament, pero se adapta a stack ligero/autocontenido según `AGENTS.md` manteniendo el mismo alcance funcional.

## Tareas
1. [x] Scaffold del proyecto y repositorio.
2. [x] Modelo de datos SQLite: `customers`, `inventory_items`, `recipes`, `recipe_ingredients`, `orders`, `order_items`, `invoices`, `invoice_items`.
3. [x] Capa de almacenamiento/servicios: CRUD de clientes e inventario, recetas con ingredientes, costeo de receta, cotización de pedido, registro de pedidos, descuento de inventario al confirmar, generación de factura desde pedido.
4. [x] CLI `reposteria` con subcomandos: `init-db`, clientes (`customer add/list`), inventario (`inventory add/list/adjust`), recetas (`recipe add/list/cost`), pedidos (`order create/list/quote/show`), facturas (`invoice create/show/list`).
5. [x] Pruebas unitarias/integración de storage y CLI.
6. [x] README con uso y comando de tests; verificación sin TODO/FIXME.

## Criterios de aceptación
- Base SQLite creada con todas las entidades requeridas y relaciones básicas. ✓
- Se pueden registrar recetas con ingredientes y calcular su costo/cotización. ✓
- Se pueden gestionar clientes, pedidos, inventario y emitir facturas ligadas a pedidos. ✓
- Operaciones clave cubiertas por pruebas automatizadas. ✓
- Sin TODO/FIXME/stubs en código. ✓

## Comando de tests
```bash
python3 -m unittest discover -s tests -p 'test*.py' -v
```
