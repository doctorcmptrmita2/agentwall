<?php

namespace App\Filament\Resources;

use App\Filament\Resources\ApiKeyResource\Pages;
use App\Models\ApiKey;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Filament\Notifications\Notification;
use Illuminate\Support\Str;

class ApiKeyResource extends Resource
{
    protected static ?string $model = ApiKey::class;
    protected static ?string $navigationIcon = 'heroicon-o-key';
    protected static ?string $navigationGroup = 'Settings';
    protected static ?int $navigationSort = 1;

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\Components\Section::make('API Key Details')
                    ->schema([
                        Forms\Components\Select::make('team_id')
                            ->relationship('team', 'name')
                            ->required()
                            ->searchable(),
                            
                        Forms\Components\TextInput::make('name')
                            ->required()
                            ->maxLength(255)
                            ->placeholder('Production Key'),
                            
                        Forms\Components\TextInput::make('daily_budget')
                            ->numeric()
                            ->prefix('$')
                            ->placeholder('Leave empty for team default'),
                            
                        Forms\Components\TextInput::make('max_steps_per_run')
                            ->numeric()
                            ->placeholder('Leave empty for team default'),
                            
                        Forms\Components\DateTimePicker::make('expires_at')
                            ->label('Expiration Date')
                            ->placeholder('Never expires'),
                            
                        Forms\Components\Toggle::make('is_active')
                            ->default(true)
                            ->inline(false),
                            
                        Forms\Components\TagsInput::make('allowed_models')
                            ->placeholder('gpt-4o, gpt-4o-mini')
                            ->helperText('Leave empty to allow all models'),
                    ])
                    ->columns(2),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('name')
                    ->searchable()
                    ->sortable(),
                    
                Tables\Columns\TextColumn::make('key_prefix')
                    ->label('Key')
                    ->formatStateUsing(fn ($state) => $state . '...')
                    ->copyable()
                    ->copyMessage('Key prefix copied'),
                    
                Tables\Columns\TextColumn::make('team.name')
                    ->sortable(),
                    
                Tables\Columns\TextColumn::make('spent_today')
                    ->label('Spent Today')
                    ->money('usd')
                    ->sortable(),
                    
                Tables\Columns\TextColumn::make('requests_today')
                    ->label('Requests')
                    ->sortable(),
                    
                Tables\Columns\IconColumn::make('is_active')
                    ->boolean(),
                    
                Tables\Columns\TextColumn::make('last_used_at')
                    ->dateTime()
                    ->sortable()
                    ->since(),
                    
                Tables\Columns\TextColumn::make('expires_at')
                    ->dateTime()
                    ->sortable()
                    ->placeholder('Never'),
            ])
            ->filters([
                Tables\Filters\TernaryFilter::make('is_active'),
                Tables\Filters\SelectFilter::make('team')
                    ->relationship('team', 'name'),
            ])
            ->actions([
                Tables\Actions\Action::make('regenerate')
                    ->icon('heroicon-o-arrow-path')
                    ->color('warning')
                    ->requiresConfirmation()
                    ->modalHeading('Regenerate API Key')
                    ->modalDescription('This will invalidate the current key. Are you sure?')
                    ->action(function (ApiKey $record) {
                        $keyData = ApiKey::generateKey();
                        $record->update([
                            'key_prefix' => $keyData['prefix'],
                            'key_hash' => $keyData['hash'],
                        ]);
                        
                        Notification::make()
                            ->title('New API Key Generated')
                            ->body('Key: ' . $keyData['key'] . ' (copy now, shown only once!)')
                            ->success()
                            ->persistent()
                            ->send();
                    }),
                Tables\Actions\Action::make('toggle')
                    ->icon(fn (ApiKey $record) => $record->is_active ? 'heroicon-o-pause' : 'heroicon-o-play')
                    ->color(fn (ApiKey $record) => $record->is_active ? 'danger' : 'success')
                    ->label(fn (ApiKey $record) => $record->is_active ? 'Disable' : 'Enable')
                    ->action(fn (ApiKey $record) => $record->update(['is_active' => !$record->is_active])),
                Tables\Actions\EditAction::make(),
                Tables\Actions\DeleteAction::make(),
            ])
            ->bulkActions([
                Tables\Actions\BulkActionGroup::make([
                    Tables\Actions\DeleteBulkAction::make(),
                ]),
            ]);
    }

    public static function getRelations(): array
    {
        return [];
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListApiKeys::route('/'),
            'create' => Pages\CreateApiKey::route('/create'),
            'edit' => Pages\EditApiKey::route('/{record}/edit'),
        ];
    }
}
