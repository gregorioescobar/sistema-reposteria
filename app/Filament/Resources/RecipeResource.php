<?php

namespace App\Filament\Resources;

use App\Filament\Resources\RecipeResource\Pages;
use App\Filament\Resources\RecipeResource\RelationManagers;
use App\Models\Recipe;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\SoftDeletingScope;

class RecipeResource extends Resource
{
    protected static ?string $model = Recipe::class;

    protected static ?string $navigationIcon = 'heroicon-o-receipt';

    protected static ?string $navigationLabel = 'Recetas';

    protected static ?string $pluralModelLabel = 'Recetas';

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\Components\TextInput::make('name')
                    ->required()
                    ->maxLength(255),
                Forms\Components\TextInput::make('yield_units')
                    ->required()
                    ->numeric()
                    ->default(1),
                Forms\Components\TextInput::make('cost_per_unit')
                    ->numeric()
                    ->prefix('$')
                    ->dehydrated(false),
                Forms\Components\TextInput::make('suggested_price')
                    ->numeric()
                    ->prefix('$'),
                Forms\Components\Textarea::make('notes'),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('name')
                    ->searchable()
                    ->sortable(),
                Tables\Columns\TextColumn::make('yield_units')
                    ->label('Rendimiento'),
                Tables\Columns\TextColumn::make('cost_per_unit')
                    ->money('USD')
                    ->label('Costo/unit.'),
                Tables\Columns\TextColumn::make('suggested_price')
                    ->money('USD')
                    ->label('Precio sugerido'),
                Tables\Columns\TextColumn::make('created_at')
                    ->dateTime()
                    ->sortable(),
            ])
            ->filters([])
            ->actions([
                Tables\Actions\ViewAction::class,
                Tables\Actions\EditAction::class,
            ])
            ->bulkActions([]);
    }

    public static function getRelations(): array
    {
        return [
            RelationManagers\RecipeIngredientsRelationManager::class,
        ];
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListRecipes::route('/'),
            'create' => Pages\CreateRecipe::route('/create'),
            'edit' => Pages\EditRecipe::route('/{record}/edit'),
            'view' => Pages\ViewRecipe::route('/{record}'),
        ];
    }
}
