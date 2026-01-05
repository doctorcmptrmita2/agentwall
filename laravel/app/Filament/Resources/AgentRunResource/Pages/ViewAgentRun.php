<?php

namespace App\Filament\Resources\AgentRunResource\Pages;

use App\Filament\Resources\AgentRunResource;
use Filament\Resources\Pages\ViewRecord;
use Filament\Infolists\Infolist;
use Filament\Infolists\Components\Section;
use Filament\Infolists\Components\TextEntry;
use Filament\Infolists\Components\IconEntry;
use Filament\Infolists\Components\Grid;

class ViewAgentRun extends ViewRecord
{
    protected static string $resource = AgentRunResource::class;

    public function infolist(Infolist $infolist): Infolist
    {
        return $infolist
            ->schema([
                Section::make('Run Information')
                    ->schema([
                        Grid::make(3)
                            ->schema([
                                TextEntry::make('run_id')
                                    ->label('Run ID')
                                    ->copyable(),
                                TextEntry::make('status')
                                    ->badge()
                                    ->color(fn (string $state): string => match ($state) {
                                        'running' => 'warning',
                                        'completed' => 'success',
                                        'failed', 'killed' => 'danger',
                                        default => 'gray',
                                    }),
                                TextEntry::make('model')
                                    ->badge()
                                    ->color('info'),
                            ]),
                    ]),
                    
                Section::make('Metrics')
                    ->schema([
                        Grid::make(4)
                            ->schema([
                                TextEntry::make('step_count')
                                    ->label('Steps'),
                                TextEntry::make('total_tokens')
                                    ->label('Tokens')
                                    ->numeric(),
                                TextEntry::make('total_cost')
                                    ->label('Cost')
                                    ->money('usd'),
                                TextEntry::make('total_latency_ms')
                                    ->label('Latency')
                                    ->suffix(' ms'),
                            ]),
                    ]),
                    
                Section::make('Safety')
                    ->schema([
                        Grid::make(3)
                            ->schema([
                                IconEntry::make('loop_detected')
                                    ->label('Loop Detected')
                                    ->boolean(),
                                IconEntry::make('budget_exceeded')
                                    ->label('Budget Exceeded')
                                    ->boolean(),
                                TextEntry::make('kill_reason')
                                    ->label('Kill Reason')
                                    ->placeholder('N/A'),
                            ]),
                    ]),
                    
                Section::make('Timing')
                    ->schema([
                        Grid::make(2)
                            ->schema([
                                TextEntry::make('started_at')
                                    ->dateTime(),
                                TextEntry::make('ended_at')
                                    ->dateTime()
                                    ->placeholder('Still running'),
                            ]),
                    ]),
                    
                Section::make('Context')
                    ->schema([
                        Grid::make(2)
                            ->schema([
                                TextEntry::make('team.name')
                                    ->label('Team'),
                                TextEntry::make('apiKey.name')
                                    ->label('API Key')
                                    ->placeholder('Unknown'),
                            ]),
                    ]),
            ]);
    }
}
