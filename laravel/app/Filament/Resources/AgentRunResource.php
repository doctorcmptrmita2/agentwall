<?php

namespace App\Filament\Resources;

use App\Filament\Resources\AgentRunResource\Pages;
use App\Models\AgentRun;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Filament\Notifications\Notification;

class AgentRunResource extends Resource
{
    protected static ?string $model = AgentRun::class;
    protected static ?string $navigationIcon = 'heroicon-o-play';
    protected static ?string $navigationGroup = 'Monitoring';
    protected static ?int $navigationSort = 1;
    protected static ?string $navigationLabel = 'Agent Runs';

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                Forms\Components\Section::make('Run Details')
                    ->schema([
                        Forms\Components\TextInput::make('run_id')
                            ->hidden(),
                        
                        Forms\Components\Select::make('status')
                            ->label('Status')
                            ->options([
                                'running' => 'Running',
                                'completed' => 'Completed',
                                'failed' => 'Failed',
                                'killed' => 'Killed',
                            ])
                            ->default('running')
                            ->required(),
                        
                        Forms\Components\TextInput::make('model')
                            ->label('Model')
                            ->placeholder('gpt-4')
                            ->default('gpt-4')
                            ->required(),
                        
                        Forms\Components\TextInput::make('agent_name')
                            ->label('Agent Name')
                            ->placeholder('My Agent')
                            ->required(),
                        
                        Forms\Components\TextInput::make('step_count')
                            ->label('Step Count')
                            ->numeric()
                            ->default(0)
                            ->minValue(0),
                        
                        Forms\Components\TextInput::make('total_tokens')
                            ->label('Total Tokens')
                            ->numeric()
                            ->default(0)
                            ->minValue(0),
                        
                        Forms\Components\TextInput::make('total_cost')
                            ->label('Total Cost')
                            ->numeric()
                            ->prefix('$')
                            ->default(0)
                            ->minValue(0)
                            ->step(0.01),
                        
                        Forms\Components\TextInput::make('total_latency_ms')
                            ->label('Latency (ms)')
                            ->numeric()
                            ->default(0)
                            ->minValue(0),
                        
                        Forms\Components\Checkbox::make('loop_detected')
                            ->label('Loop Detected'),
                        
                        Forms\Components\Checkbox::make('budget_exceeded')
                            ->label('Budget Exceeded'),
                        
                        Forms\Components\TextInput::make('kill_reason')
                            ->label('Kill Reason')
                            ->placeholder('Optional - reason for killing the run'),
                    ])
                    ->columns(2),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('run_id')
                    ->label('Run ID')
                    ->searchable()
                    ->copyable()
                    ->limit(12),
                    
                Tables\Columns\BadgeColumn::make('status')
                    ->colors([
                        'warning' => 'running',
                        'success' => 'completed',
                        'danger' => fn ($state) => in_array($state, ['failed', 'killed']),
                    ]),
                    
                Tables\Columns\TextColumn::make('model')
                    ->sortable()
                    ->badge()
                    ->color('gray'),
                    
                Tables\Columns\TextColumn::make('step_count')
                    ->label('Steps')
                    ->sortable(),
                    
                Tables\Columns\TextColumn::make('total_tokens')
                    ->label('Tokens')
                    ->numeric()
                    ->sortable(),
                    
                Tables\Columns\TextColumn::make('total_cost')
                    ->label('Cost')
                    ->money('usd')
                    ->sortable(),
                    
                Tables\Columns\IconColumn::make('loop_detected')
                    ->label('Loop')
                    ->boolean()
                    ->trueIcon('heroicon-o-arrow-path')
                    ->falseIcon('heroicon-o-minus')
                    ->trueColor('danger')
                    ->falseColor('gray'),
                    
                Tables\Columns\TextColumn::make('kill_reason')
                    ->label('Kill Reason')
                    ->placeholder('-')
                    ->limit(20),
                    
                Tables\Columns\TextColumn::make('started_at')
                    ->dateTime()
                    ->sortable()
                    ->since(),
                    
                Tables\Columns\TextColumn::make('team.name')
                    ->sortable(),
            ])
            ->defaultSort('started_at', 'desc')
            ->filters([
                Tables\Filters\SelectFilter::make('status')
                    ->options([
                        'running' => 'Running',
                        'completed' => 'Completed',
                        'failed' => 'Failed',
                        'killed' => 'Killed',
                    ]),
                Tables\Filters\TernaryFilter::make('loop_detected')
                    ->label('Loop Detected'),
                Tables\Filters\SelectFilter::make('team')
                    ->relationship('team', 'name'),
            ])
            ->actions([
                Tables\Actions\Action::make('kill')
                    ->icon('heroicon-o-stop')
                    ->color('danger')
                    ->visible(fn (AgentRun $record) => $record->status === 'running')
                    ->requiresConfirmation()
                    ->modalHeading('Kill This Run')
                    ->modalDescription('This will immediately stop the agent. Are you sure?')
                    ->modalSubmitActionLabel('Kill Run')
                    ->form([
                        Forms\Components\TextInput::make('reason')
                            ->label('Kill Reason')
                            ->required()
                            ->placeholder('Manual kill from dashboard'),
                    ])
                    ->action(function (AgentRun $record, array $data) {
                        $record->update([
                            'status' => 'killed',
                            'kill_reason' => 'dashboard:' . $data['reason'],
                            'ended_at' => now(),
                        ]);
                        
                        Notification::make()
                            ->title('Run Killed')
                            ->body("Run {$record->run_id} has been terminated.")
                            ->success()
                            ->send();
                    }),
                    
                Tables\Actions\ViewAction::make(),
            ])
            ->bulkActions([
                Tables\Actions\BulkActionGroup::make([
                    Tables\Actions\BulkAction::make('killAll')
                        ->label('Kill Selected')
                        ->icon('heroicon-o-stop')
                        ->color('danger')
                        ->requiresConfirmation()
                        ->action(function ($records) {
                            $records->each(function ($record) {
                                if ($record->status === 'running') {
                                    $record->update([
                                        'status' => 'killed',
                                        'kill_reason' => 'dashboard:bulk_kill',
                                        'ended_at' => now(),
                                    ]);
                                }
                            });
                            
                            Notification::make()
                                ->title('Runs Killed')
                                ->success()
                                ->send();
                        }),
                ]),
            ])
            ->poll('5s');
    }

    public static function getRelations(): array
    {
        return [];
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListAgentRuns::route('/'),
        ];
    }
    
    public static function getNavigationBadge(): ?string
    {
        $count = static::getModel()::where('status', 'running')->count();
        return $count > 0 ? (string) $count : null;
    }
    
    public static function getNavigationBadgeColor(): ?string
    {
        $count = static::getModel()::where('status', 'running')->count();
        return $count > 5 ? 'warning' : 'success';
    }
}
