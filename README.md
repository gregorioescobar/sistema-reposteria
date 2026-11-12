# Sistema para Repostería

Sistema completo de gestión para repostería construido con **Laravel 11**, **Filament 3** y **SQLite**. Incluye panel de administración para clientes, inventario, recetas, pedidos y facturas.

## Alcance
- **Clientes:** alta, edición y listado.
- **Inventario:** insumos con unidad, costo y cantidad; ajustes de stock.
- **Recetas:** ingredientes por insumo, rendimiento, costo total/unitario y precio sugerido (cotización con margen).
- **Pedidos:** cotización, creación (borrador o confirmado con descuento automático de inventario) y consulta.
- **Facturas:** emisión desde pedidos confirmados, numeración única y consulta.

## Stack
- PHP 8.3+
- Laravel 11
- Filament 3 (panel de administración)
- SQLite (base de datos en un solo archivo)
- PHPUnit (pruebas automatizadas)

## Requisitos
- PHP 8.3+
- Composer
- Extensiones PHP: sqlite3, mbstring, bcmath, etc.

## Instalación
```bash
# Clonar el repositorio
git clone https://github.com/gregorioescobar/sistema-reposteria.git
cd sistema-reposteria

# Instalar dependencias
composer install

# Generar clave de aplicación
php artisan key:generate

# La base de datos SQLite se crea automáticamente
touch database/database.sqlite

# Ejecutar migraciones
php artisan migrate

# Iniciar el servidor
php artisan serve
```

Luego accede a http://localhost:8000/admin para el panel de Filament.

## Uso
Desde el panel de administración (`/admin`):
1. Agrega clientes en **Clientes**.
2. Agrega insumos en **Inventario** (nombre, unidad, costo, cantidad).
3. Crea recetas en **Recetas** con sus ingredientes.
4. Crea pedidos en **Pedidos** (selecciona cliente, agrega ítems de receta).
5. Confirma pedidos para descontar inventario automáticamente.
6. Genera facturas en **Facturas** desde pedidos confirmados.

## Pruebas
```bash
php artisan test
```

Ejecuta las 12 pruebas unitarias que cubren modelos, relaciones y lógica de negocio (costo de receta, confirmación de pedido, unicidad de número de factura, etc.).

## Estructura
```
app/
  Models/           - Modelos Eloquent (Customer, InventoryItem, Recipe, etc.)
  Filament/
    Resources/      - Recursos CRUD de Filament (CustomerResource, etc.)
database/
  migrations/       - Migraciones de base de datos
tests/
  Unit/             - Pruebas unitarias (12 tests)
```
# Ajuste menor para PR
