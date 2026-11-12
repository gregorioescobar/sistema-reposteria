<?php

use App\Models\InventoryItem;
use App\Models\Recipe;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class RecipeTest extends TestCase
{
    use RefreshDatabase;
    public function test_recipe_can_be_created(): void
    {
        $recipe = Recipe::create([
            'name' => 'Pastel de Chocolate',
            'yield_units' => 2,
            'cost_per_unit' => 0.0000,
            'suggested_price' => 15.0000,
        ]);

        $this->assertDatabaseHas('recipes', [
            'name' => 'Pastel de Chocolate',
        ]);
        $this->assertEquals(2, $recipe->yield_units);
    }

    public function test_recipe_calculates_cost_from_ingredients(): void
    {
        $recipe = Recipe::create([
            'name' => 'Galletas',
            'yield_units' => 10,
            'cost_per_unit' => 0.0000,
            'suggested_price' => 0.0000,
        ]);

        $harina = InventoryItem::create([
            'name' => 'Harina',
            'unit' => 'kg',
            'cost' => 2.0000,
            'quantity' => 10.0000,
        ]);

        $azucar = InventoryItem::create([
            'name' => 'Azúcar',
            'unit' => 'kg',
            'cost' => 1.5000,
            'quantity' => 5.0000,
        ]);

        $recipe->ingredients()->attach($harina->id, ['quantity' => 1.5000]);
        $recipe->ingredients()->attach($azucar->id, ['quantity' => 0.5000]);

        $recipe->refresh();

        $expectedCost = (1.5 * 2.0) + (0.5 * 1.5); // 3.0 + 0.75 = 3.75
        $this->assertEqualsWithDelta($expectedCost, $recipe->calculateCost(), 0.0001);
        $this->assertEqualsWithDelta($expectedCost / 10, $recipe->calculateCostPerUnit(), 0.0001);
    }
}
