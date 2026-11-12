<?php

namespace App\Filament\Resources\CustomerResource\RelationManagers;

use Filament\Resources\RelationManagers\RelationManager;

class OrdersRelationManager extends RelationManager
{
    protected static string $relationship = 'orders';

    protected static ?string $title = 'Pedidos';

    public function table(\Filament\Tables\Table $table): \Filament\Tables\Table
    {
        return $table
            ->columns([
                \Filament\Tables\Columns\TextColumn::make('id'),
                \Filament\Tables\Columns\TextColumn::make('status'),
                \Filament\Tables\Columns\TextColumn::make('total')->money('USD'),
            ])
            ->actions([]);
    }
}
