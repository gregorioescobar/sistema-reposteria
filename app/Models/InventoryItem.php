<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class InventoryItem extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'unit',
        'cost',
        'quantity',
    ];

    protected $casts = [
        'cost' => 'decimal:4',
        'quantity' => 'decimal:4',
    ];

    public function recipes(): BelongsToMany
    {
        return $this->belongsToMany(Recipe::class, 'recipe_ingredients')
            ->using(RecipeIngredient::class)
            ->withPivot('quantity')
            ->withTimestamps();
    }
}
