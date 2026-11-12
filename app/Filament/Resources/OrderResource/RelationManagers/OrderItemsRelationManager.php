<?php

namespace App\Filament\Resources\OrderResource\RelationManagers;

use Filament\Resources\RelationManagers\RelationManager;

class OrderItemsRelationManager extends RelationManager
{
    protected static string $relationship = 'items';

    protected static ?string $title = 'Items del Pedido';

    public function table(\Filament\Tables\Table $table): \Filament\Tables\Table
    {
        return $table
            ->columns([
                \Filament\Tables\Columns\TextColumn::make('recipe.name'),
                \Filament\Tables\Columns\TextColumn::make('quantity'),
                \Filament\Tables\Columns\TextColumn::make('unit_price')->money('USD'),
                \Filament\Tables\Columns\TextColumn::make('subtotal')->money('USD'),
            ])
            ->actions([]);
    }
}
