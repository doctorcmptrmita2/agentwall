<?php

namespace App\Filament\Resources;

use App\Filament\Resources\BudgetPolicyResource\Pages;
use App\Models\BudgetPolicy;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Filament\Notifications\Notification;

class BudgetPolicyResource extends Resource
{
    protected static ?string $model = BudgetPolicy::class;
    protected static ?string $navigationIcon = 'heroicon-o-currency-dollar';
    protected static ?string $navigationGroup = 'Governance';
    protected static ?int $navigationSort = 2;
    protected static ?string $navigationLabel = 'Budget Policies';

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\Components\Section::make('Policy Details')
                    ->schema([
                        Forms\Components\TextInput::make('name')
                            ->label('Policy Name')
                            ->required()
                            ->placeholder('Default Budget Policy')
                            ->maxLength(255),
                        
                        Forms\Components\Textarea::make('description')
                            ->label('Description')
                            ->placeholder('Budget limits for production agents')
                            ->rows(2),
                        
                        Forms\Components\Toggle::make('is_active')
                            ->label('Active')
                            ->default(true)
                            ->helperText('Only active policies are enforced'),
                    ])
                    ->columns(1),
                
                Forms\Components\Section::make('Budget Limits')
                    ->description('Set spending limits for agent runs')
                    ->schema([
                        Forms\Components\TextInput::make('per_run_limit')
                            ->label('Per-Run Limit')
                            ->numeric()
                            ->prefix('$')
                            ->default(10)
                            ->required()
                            ->helperText('Maximum cost per single agent run'),
                        
                        Forms\Components\TextInput::make('daily_limit')
                            ->label('Daily Limit')
                            ->numeric()
                            ->prefix('$')
                            ->default(100)
                            ->required()
                            ->helperText('Maximum daily spending'),
                        
                        Forms\Components\TextInput::make('monthly_limit')
                            ->label('Monthly Limit')
                            ->numeric()
                            ->prefix('$')
                            ->default(3000)
                            ->required()
                            ->helperText('Maximum monthly spending'),
                    ])
                    ->columns(3),
                
                Forms\Components\Section::make('Alerts & Actions')
                    ->schema([
                        Forms\Components\TextInput::make('alert_threshold')
                            ->label('Alert Threshold')
                            ->numeric()
                            ->prefix('$')
                            ->default(5)
                            ->helperText('Send alert when run cost exceeds this'),
                        
                        Forms\Components\Toggle::make('auto_kill_enabled')
                            ->label('Auto-Kill on Budget Exceeded')
                            ->default(true)
                            ->helperText('Automatically stop runs that exceed budget'),
                    ])
                    ->columns(2),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('name')
                    ->label('Policy Name')
                    ->searchable()
                    ->sortable(),
                
                Tables\Columns\IconColumn::make('is_active')
                    ->label('Active')
                    ->boolean(),
                
                Tables\Columns\TextColumn::make('per_run_limit')
                    ->label('Per-Run')
                    ->money('usd')
                    ->sortable(),
                
                Tables\Columns\TextColumn::make('daily_limit')
                    ->label('Daily')
                    ->money('usd')
                    ->sortable(),
                
                Tables\Columns\TextColumn::make('monthly_limit')
                    ->label('Monthly')
                    ->money('usd')
                    ->sortable(),
                
                Tables\Columns\IconColumn::make('auto_kill_enabled')
                    ->label('Auto-Kill')
                    ->boolean()
                    ->trueIcon('heroicon-o-stop')
                    ->falseIcon('heroicon-o-minus')
                    ->trueColor('danger')
                    ->falseColor('gray'),
                
                Tables\Columns\TextColumn::make('team.name')
                    ->label('Team')
                    ->sortable(),
                
                Tables\Columns\TextColumn::make('updated_at')
                    ->label('Updated')
                    ->dateTime()
                    ->sortable()
                    ->since(),
            ])
            ->defaultSort('updated_at', 'desc')
            ->filters([
                Tables\Filters\TernaryFilter::make('is_active')
                    ->label('Active'),
                Tables\Filters\TernaryFilter::make('auto_kill_enabled')
                    ->label('Auto-Kill'),
            ])
            ->actions([
                Tables\Actions\EditAction::make(),
                Tables\Actions\Action::make('duplicate')
                    ->icon('heroicon-o-document-duplicate')
                    ->color('gray')
                    ->action(function (BudgetPolicy $record) {
                        $new = $record->replicate();
                        $new->name = $record->name . ' (Copy)';
                        $new->save();
                        
                        Notification::make()
                            ->title('Policy Duplicated')
                            ->success()
                            ->send();
                    }),
            ])
            ->bulkActions([
                Tables\Actions\BulkActionGroup::make([
                    Tables\Actions\DeleteBulkAction::make(),
                    Tables\Actions\BulkAction::make('activate')
                        ->label('Activate')
                        ->icon('heroicon-o-check')
                        ->action(fn ($records) => $records->each->update(['is_active' => true])),
                    Tables\Actions\BulkAction::make('deactivate')
                        ->label('Deactivate')
                        ->icon('heroicon-o-x-mark')
                        ->action(fn ($records) => $records->each->update(['is_active' => false])),
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
            'index' => Pages\ListBudgetPolicies::route('/'),
            'create' => Pages\CreateBudgetPolicy::route('/create'),
            'edit' => Pages\EditBudgetPolicy::route('/{record}/edit'),
        ];
    }
}
