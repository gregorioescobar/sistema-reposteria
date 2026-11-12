<?php

use App\Models\InventoryItem;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class InventoryItemTest extends TestCase
{
    use RefreshDatabase;
    public function test_inventory_item_can_be_created(): void
    {
        $item = InventoryItem::create([
            'name' => 'Harina',
            'unit' => 'kg',
            'cost' => 2.0000,
            'quantity' => 10.0000,
        ]);

        $this->assertDatabaseHas('inventory_items', [
            'name' => 'Harina',
            'unit' => 'kg',
        ]);
        $this->assertEquals(2.0000, $item->cost);
        $this->assertEquals(10.0000, $item->quantity);
    }

    public function test_inventory_item_quantity_can_be_adjusted(): void
    {
        $item = InventoryItem::create([
            'name' => 'Azúcar',
            'unit' => 'kg',
            'cost' => 1.5000,
            'quantity' => 5.0000,
        ]);

        $item->decrement('quantity', 2.0000);
        $item->refresh();

        $this->assertEquals(3.0000, $item->quantity);
    }
}
