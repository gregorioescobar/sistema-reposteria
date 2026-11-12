<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Recipe extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'yield_units',
        'cost_per_unit',
        'suggested_price',
        'notes',
    ];

    protected $casts = [
        'cost_per_unit' => 'decimal:4',
        'suggested_price' => 'decimal:4',
    ];

    public function ingredients(): BelongsToMany
    {
        return $this->belongsToMany(InventoryItem::class, 'recipe_ingredients')->withTimestamps();
    }

    public function recipeIngredients(): HasMany
    {
        return $this->hasMany(RecipeIngredient::class);
    }

    public function orderItems(): HasMany
    {
        return $this->hasMany(OrderItem::class);
    }

    public function calculateCost(): float
    {
        $total = 0.0;
        foreach ($this->recipeIngredients as $ri) {
            $total += (float) $ri->quantity * (float) $ri->inventoryItem->cost;
        }
        return $total;
    }

    public function calculateCostPerUnit(): float
    {
        if ($this->yield_units <= 0) {
            return 0.0;
        }
        return $this->calculateCost() / $this->yield_units;
    }
}
