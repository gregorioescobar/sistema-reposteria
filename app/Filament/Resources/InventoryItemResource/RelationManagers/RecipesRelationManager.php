<?php

namespace App\Filament\Resources\InventoryItemResource\RelationManagers;

use Filament\Resources\RelationManagers\RelationManager;

class RecipesRelationManager extends RelationManager
{
    protected static string $relationship = 'recipes';

    protected static ?string $title = 'Recetas';

    public function table(\Filament\Tables\Table $table): \Filament\Tables\Table
    {
        return $table
            ->columns([
                \Filament\Tables\Columns\TextColumn::make('name'),
                \Filament\Tables\Columns\TextColumn::make('cost_per_unit')->money('USD'),
            ])
            ->actions([]);
    }
}
