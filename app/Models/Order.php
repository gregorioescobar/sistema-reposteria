<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;

class Order extends Model
{
    use HasFactory;

    protected $fillable = [
        'customer_id',
        'subtotal',
        'discount',
        'total',
        'status',
        'notes',
    ];

    protected $casts = [
        'subtotal' => 'decimal:4',
        'discount' => 'decimal:4',
        'total' => 'decimal:4',
    ];

    public function customer(): BelongsTo
    {
        return $this->belongsTo(Customer::class);
    }

    public function items(): HasMany
    {
        return $this->hasMany(OrderItem::class);
    }

    public function invoice(): HasOne
    {
        return $this->hasOne(Invoice::class);
    }

    public function calculateTotals(): void
    {
        $subtotal = $this->items->sum('subtotal');
        $this->subtotal = $subtotal;
        $this->total = $subtotal - $this->discount;
        $this->save();
    }

    public function confirmInventory(): bool
    {
        if ($this->status !== 'draft') {
            return false;
        }
        foreach ($this->items as $item) {
            $recipe = $item->recipe;
            foreach ($recipe->recipeIngredients as $ri) {
                $inventoryItem = $ri->inventoryItem;
                $needed = (float) $ri->quantity * (float) $item->quantity;
                if ((float) $inventoryItem->quantity < $needed) {
                    return false;
                }
                $inventoryItem->decrement('quantity', $needed);
            }
        }
        $this->status = 'confirmed';
        $this->save();
        return true;
    }
}
