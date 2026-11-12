<?php

namespace App\Filament\Resources\RecipeResource\RelationManagers;

use Filament\Resources\RelationManagers\RelationManager;

class RecipeIngredientsRelationManager extends RelationManager
{
    protected static string $relationship = 'ingredients';

    protected static ?string $title = 'Ingredientes';

    public function table(\Filament\Tables\Table $table): \Filament\Tables\Table
    {
        return $table
            ->columns([
                \Filament\Tables\Columns\TextColumn::make('inventoryItem.name'),
                \Filament\Tables\Columns\TextColumn::make('pivot.quantity'),
            ])
            ->actions([]);
    }
}
