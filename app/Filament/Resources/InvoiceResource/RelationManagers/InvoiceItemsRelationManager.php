<?php

namespace App\Filament\Resources\InvoiceResource\RelationManagers;

use Filament\Resources\RelationManagers\RelationManager;

class InvoiceItemsRelationManager extends RelationManager
{
    protected static string $relationship = 'items';

    protected static ?string $title = 'Items de Factura';

    public function table(\Filament\Tables\Table $table): \Filament\Tables\Table
    {
        return $table
            ->columns([
                \Filament\Tables\Columns\TextColumn::make('description'),
                \Filament\Tables\Columns\TextColumn::make('quantity'),
                \Filament\Tables\Columns\TextColumn::make('unit_price')->money('USD'),
                \Filament\Tables\Columns\TextColumn::make('subtotal')->money('USD'),
            ])
            ->actions([]);
    }
}
