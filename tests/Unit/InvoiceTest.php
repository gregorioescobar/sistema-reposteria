<?php

use App\Models\Customer;
use App\Models\Invoice;
use App\Models\Order;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class InvoiceTest extends TestCase
{
    use RefreshDatabase;
    public function test_invoice_can_be_created_from_order(): void
    {
        $customer = Customer::create([
            'name' => 'Cliente Factura',
        ]);

        $order = $customer->orders()->create([
            'subtotal' => 50.0000,
            'discount' => 0.0000,
            'total' => 50.0000,
            'status' => 'confirmed',
        ]);

        $invoice = $order->invoice()->create([
            'invoice_number' => 'FAC-001',
            'total' => 50.0000,
            'issued_at' => now(),
        ]);

        $this->assertDatabaseHas('invoices', [
            'invoice_number' => 'FAC-001',
        ]);
        $this->assertEquals($order->id, $invoice->order_id);
        $this->assertEquals(50.0000, $invoice->total);
    }

    public function test_invoice_number_is_unique(): void
    {
        $customer = Customer::create([
            'name' => 'Cliente Dup',
        ]);

        $order1 = $customer->orders()->create([
            'subtotal' => 10.0000,
            'discount' => 0.0000,
            'total' => 10.0000,
            'status' => 'confirmed',
        ]);

        $order2 = $customer->orders()->create([
            'subtotal' => 20.0000,
            'discount' => 0.0000,
            'total' => 20.0000,
            'status' => 'confirmed',
        ]);

        Invoice::create([
            'order_id' => $order1->id,
            'invoice_number' => 'FAC-DUP',
            'total' => 10.0000,
            'issued_at' => now(),
        ]);

        $this->expectException(\Illuminate\Database\QueryException::class);
        Invoice::create([
            'order_id' => $order2->id,
            'invoice_number' => 'FAC-DUP',
            'total' => 20.0000,
            'issued_at' => now(),
        ]);
    }
}
