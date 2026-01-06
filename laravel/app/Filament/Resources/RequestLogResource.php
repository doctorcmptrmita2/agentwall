<?php

namespace App\Filament\Resources;

use App\Filament\Resources\RequestLogResource\Pages;
use App\Models\RequestLog;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Filament\Tables\Filters\SelectFilter;
use Filament\Tables\Filters\Filter;
use Illuminate\Database\Eloquent\Builder;

class RequestLogResource extends Resource
{
    protected static ?string $model = RequestLog::class;
    protected static ?string $navigationIcon = 'heroicon-o-document-text';
    protected static ?string $navigationGroup = 'Logs & Analytics';
    protected static ?string $navigationLabel = 'Request Logs';
    protected static ?int $navigationSort = 1;

    public static function form(Form $form): Form
    {
        return $form->schema([
            Forms\Components\Section::make('Request Details')->schema([
                Forms\Components\TextInput::make('request_id')->disabled(),
                Forms\Components\TextInput::make('run_id')->disabled(),
                Forms\Components\TextInput::make('model')->disabled(),
                Forms\Components\TextInput::make('provider')->disabled(),
            ])->columns(2),
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('created_at')
                    ->label('Time')
                    ->dateTime('M d, H:i:s')
                    ->sortable(),

                Tables\Columns\TextColumn::make('model')
                    ->searchable()
                    ->sortable()
                    ->limit(20),

                Tables\Columns\BadgeColumn::make('provider')
                    ->colors([
                        'success' => 'openai',
                        'info' => 'openrouter',
                        'warning' => 'groq',
                        'primary' => 'deepseek',
                        'danger' => 'mistral',
                    ]),

                Tables\Columns\TextColumn::make('total_tokens')
                    ->label('Tokens')
                    ->numeric()
                    ->sortable(),

                Tables\Columns\TextColumn::make('cost_usd')
                    ->label('Cost')
                    ->money('usd', 6)
                    ->sortable(),

                Tables\Columns\TextColumn::make('latency_ms')
                    ->label('Latency')
                    ->suffix('ms')
                    ->sortable()
                    ->color(fn ($state) => $state > 5000 ? 'danger' : ($state > 2000 ? 'warning' : 'success')),

                Tables\Columns\BadgeColumn::make('status_code')
                    ->label('Status')
                    ->colors([
                        'success' => fn ($state) => $state >= 200 && $state < 300,
                        'warning' => fn ($state) => $state >= 400 && $state < 500,
                        'danger' => fn ($state) => $state >= 500,
                    ]),

                Tables\Columns\IconColumn::make('stream')
                    ->boolean()
                    ->label('Stream'),

                Tables\Columns\IconColumn::make('dlp_triggered')
                    ->boolean()
                    ->label('DLP')
                    ->trueIcon('heroicon-o-shield-exclamation')
                    ->falseIcon('heroicon-o-shield-check')
                    ->trueColor('danger')
                    ->falseColor('success'),

                Tables\Columns\IconColumn::make('loop_detected')
                    ->boolean()
                    ->label('Loop')
                    ->trueIcon('heroicon-o-arrow-path')
                    ->trueColor('danger'),

                Tables\Columns\TextColumn::make('run_id')
                    ->label('Run')
                    ->limit(8)
                    ->searchable()
                    ->copyable(),
            ])
            ->defaultSort('created_at', 'desc')
            ->filters([
                SelectFilter::make('provider')
                    ->options([
                        'openai' => 'OpenAI',
                        'openrouter' => 'OpenRouter',
                        'groq' => 'Groq',
                        'deepseek' => 'DeepSeek',
                        'mistral' => 'Mistral',
                        'ollama' => 'Ollama',
                    ]),

                SelectFilter::make('status')
                    ->options([
                        'success' => 'Success (2xx)',
                        'error' => 'Error (4xx/5xx)',
                    ])
                    ->query(function (Builder $query, array $data) {
                        return match ($data['value']) {
                            'success' => $query->where('status_code', '>=', 200)->where('status_code', '<', 300),
                            'error' => $query->where('status_code', '>=', 400),
                            default => $query,
                        };
                    }),

                Filter::make('dlp_triggered')
                    ->label('DLP Triggered')
                    ->query(fn (Builder $query) => $query->where('dlp_triggered', true)),

                Filter::make('loop_detected')
                    ->label('Loop Detected')
                    ->query(fn (Builder $query) => $query->where('loop_detected', true)),

                Filter::make('today')
                    ->label('Today')
                    ->query(fn (Builder $query) => $query->whereDate('created_at', today())),
            ])
            ->actions([
                Tables\Actions\ViewAction::make(),
            ])
            ->bulkActions([])
            ->poll('10s');
    }

    public static function getRelations(): array
    {
        return [];
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListRequestLogs::route('/'),
            'view' => Pages\ViewRequestLog::route('/{record}'),
        ];
    }

    public static function getNavigationBadge(): ?string
    {
        return static::getModel()::today()->count();
    }

    public static function getNavigationBadgeColor(): ?string
    {
        return 'primary';
    }
}
