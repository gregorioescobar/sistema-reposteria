<?php

use App\Models\Customer;
use App\Models\InventoryItem;
use App\Models\Order;
use App\Models\Recipe;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class OrderTest extends TestCase
{
    use RefreshDatabase;
    public function test_order_can_be_created_and_confirmed(): void
    {
        $customer = Customer::create([
            'name' => 'Cliente Pedido',
            'phone' => '555-0103',
        ]);

        $recipe = Recipe::create([
            'name' => 'Tarta',
            'yield_units' => 1,
            'cost_per_unit' => 10.0000,
            'suggested_price' => 20.0000,
        ]);

        $harina = InventoryItem::create([
            'name' => 'Harina',
            'unit' => 'kg',
            'cost' => 2.0000,
            'quantity' => 100.0000,
        ]);

        $recipe->ingredients()->attach($harina->id, ['quantity' => 0.5000]);

        $order = $customer->orders()->create([
            'subtotal' => 0.0000,
            'discount' => 0.0000,
            'total' => 0.0000,
            'status' => 'draft',
        ]);

        $order->items()->create([
            'recipe_id' => $recipe->id,
            'quantity' => 2,
            'unit_price' => 20.0000,
            'subtotal' => 40.0000,
        ]);

        $order->calculateTotals();
        $order->refresh();

        $this->assertEquals(40.0000, $order->subtotal);
        $this->assertEquals(40.0000, $order->total);

        $result = $order->confirmInventory();
        $this->assertTrue($result);
        $order->refresh();
        $this->assertEquals('confirmed', $order->status);

        $harina->refresh();
        $this->assertEquals(99.0000, $harina->quantity);
    }

    public function test_order_cannot_be_confirmed_twice(): void
    {
        $customer = Customer::create([
            'name' => 'Cliente Doble',
        ]);

        $order = $customer->orders()->create([
            'subtotal' => 0.0000,
            'discount' => 0.0000,
            'total' => 0.0000,
            'status' => 'confirmed',
        ]);

        $result = $order->confirmInventory();
        $this->assertFalse($result);
    }
}
