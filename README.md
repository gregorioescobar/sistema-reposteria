# Sistema para Repostería

Sistema CLI ligero y autocontenido (Python stdlib + SQLite) para gestionar una repostería.

## Alcance
- **Clientes:** alta y listado.
- **Inventario:** insumos con unidad, costo y cantidad; ajustes de stock.
- **Recetas:** ingredientes por insumo, rendimiento, costo total/unitario y precio sugerido (cotización con margen).
- **Pedidos:** cotización, creación (borrador o confirmado con descuento de inventario) y consulta.
- **Facturas:** emisión desde pedido confirmado/borrador registrado y consulta.

> Nota: la idea original sugería PHP/Laravel/Filament; se implementó con stack ligero (Python stdlib + SQLite) según `AGENTS.md`, cubriendo el mismo alcance funcional.

## Requisitos
- Python 3.12+ (solo biblioteca estándar)

## Uso
Desde el directorio del proyecto:

```bash
# Inicializar base de datos (por defecto ./reposteria.db)
python3 -m reposteria init-db

# Clientes
python3 -m reposteria customer add --name "Ana" --phone "555-0101" --email ana@example.com
python3 -m reposteria customer list

# Inventario
python3 -m reposteria inventory add --name Harina --unit kg --cost 2.0 --quantity 10
python3 -m reposteria inventory list
python3 -m reposteria inventory adjust --id 1 --delta -0.5

# Recetas (ingredientes: item_id:cantidad,...)
python3 -m reposteria recipe add --name "Pastel" --yield-units 2 --ingredients "1:1.5"
python3 -m reposteria recipe list
python3 -m reposteria recipe cost --id 1 --margin 0.3

# Pedidos y cotización (items: recipe_id:cantidad[:precio_unitario],...)
python3 -m reposteria order quote --items "1:3" --margin 0.3
python3 -m reposteria order create --customer-id 1 --items "1:3" --confirm
python3 -m reposteria order list
python3 -m reposteria order show --id 1

# Facturas
python3 -m reposteria invoice create --order-id 1
python3 -m reposteria invoice show --id 1
python3 -m reposteria invoice list
```

Usa `--db /ruta/archivo.db` para apuntar a otra base.

## Pruebas
```bash
python3 -m unittest discover -s tests -p 'test*.py' -v
```
