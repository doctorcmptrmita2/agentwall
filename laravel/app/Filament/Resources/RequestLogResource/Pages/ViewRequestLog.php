<?php

namespace App\Filament\Resources\RequestLogResource\Pages;

use App\Filament\Resources\RequestLogResource;
use Filament\Resources\Pages\ViewRecord;
use Filament\Infolists\Infolist;
use Filament\Infolists\Components\Section;
use Filament\Infolists\Components\TextEntry;
use Filament\Infolists\Components\IconEntry;
use Filament\Infolists\Components\Grid;

class ViewRequestLog extends ViewRecord
{
    protected static string $resource = RequestLogResource::class;

    public function infolist(Infolist $infolist): Infolist
    {
        return $infolist->schema([
            Section::make('Request Info')->schema([
                Grid::make(3)->schema([
                    TextEntry::make('request_id')->label('Request ID')->copyable(),
                    TextEntry::make('run_id')->label('Run ID')->copyable(),
                    TextEntry::make('created_at')->label('Time')->dateTime(),
                ]),
                Grid::make(3)->schema([
                    TextEntry::make('model')->badge(),
                    TextEntry::make('provider')->badge()->color(fn ($state) => match($state) {
                        'openai' => 'success',
                        'openrouter' => 'info',
                        'groq' => 'warning',
                        default => 'gray',
                    }),
                    TextEntry::make('endpoint'),
                ]),
            ]),

            Section::make('Tokens & Cost')->schema([
                Grid::make(4)->schema([
                    TextEntry::make('prompt_tokens')->label('Prompt'),
                    TextEntry::make('completion_tokens')->label('Completion'),
                    TextEntry::make('total_tokens')->label('Total'),
                    TextEntry::make('cost_usd')->label('Cost')->money('usd', 6),
                ]),
            ]),

            Section::make('Performance')->schema([
                Grid::make(3)->schema([
                    TextEntry::make('latency_ms')->label('Latency')->suffix('ms'),
                    TextEntry::make('ttfb_ms')->label('TTFB')->suffix('ms'),
                    TextEntry::make('status_code')->label('Status')->badge()->color(fn ($state) => 
                        $state >= 200 && $state < 300 ? 'success' : ($state >= 400 ? 'danger' : 'warning')
                    ),
                ]),
            ]),

            Section::make('Security Flags')->schema([
                Grid::make(4)->schema([
                    IconEntry::make('stream')->boolean(),
                    IconEntry::make('dlp_triggered')->label('DLP')->boolean(),
                    IconEntry::make('loop_detected')->label('Loop')->boolean(),
                    IconEntry::make('budget_exceeded')->label('Budget')->boolean(),
                ]),
            ]),

            Section::make('Error Details')
                ->schema([
                    TextEntry::make('error_type'),
                    TextEntry::make('error_message')->columnSpanFull(),
                ])
                ->visible(fn ($record) => $record->status_code >= 400),

            Section::make('Client Info')->schema([
                Grid::make(2)->schema([
                    TextEntry::make('ip_address'),
                    TextEntry::make('user_agent')->limit(50),
                ]),
            ])->collapsed(),
        ]);
    }
}
