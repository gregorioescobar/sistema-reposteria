<?php

use App\Models\Customer;
use App\Models\Order;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class CustomerTest extends TestCase
{
    use RefreshDatabase;
    public function test_customer_can_be_created(): void
    {
        $customer = Customer::create([
            'name' => 'Ana García',
            'phone' => '555-0101',
            'email' => 'ana@example.com',
            'address' => 'Calle Falsa 123',
        ]);

        $this->assertDatabaseHas('customers', [
            'name' => 'Ana García',
            'email' => 'ana@example.com',
        ]);
        $this->assertInstanceOf(Customer::class, $customer);
    }

    public function test_customer_has_orders_relationship(): void
    {
        $customer = Customer::create([
            'name' => 'Cliente Test',
            'phone' => '555-0102',
        ]);

        $order = $customer->orders()->create([
            'subtotal' => 100.00,
            'discount' => 0.00,
            'total' => 100.00,
            'status' => 'draft',
        ]);

        $this->assertCount(1, $customer->orders);
        $this->assertEquals($order->id, $customer->orders->first()->id);
    }
}
