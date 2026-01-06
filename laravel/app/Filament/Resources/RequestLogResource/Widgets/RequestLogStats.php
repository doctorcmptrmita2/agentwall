<?php

namespace App\Filament\Resources\RequestLogResource\Widgets;

use App\Models\RequestLog;
use Filament\Widgets\StatsOverviewWidget as BaseWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class RequestLogStats extends BaseWidget
{
    protected function getStats(): array
    {
        $today = RequestLog::today();
        $thisMonth = RequestLog::thisMonth();

        return [
            Stat::make('Today Requests', $today->count())
                ->description('Total API calls today')
                ->descriptionIcon('heroicon-m-arrow-trending-up')
                ->color('primary'),

            Stat::make('Today Cost', '$' . number_format($today->sum('cost_usd'), 4))
                ->description('Total spend today')
                ->descriptionIcon('heroicon-m-currency-dollar')
                ->color('success'),

            Stat::make('Today Tokens', number_format($today->sum('total_tokens')))
                ->description('Total tokens used')
                ->descriptionIcon('heroicon-m-document-text')
                ->color('info'),

            Stat::make('Avg Latency', round($today->avg('latency_ms') ?? 0) . 'ms')
                ->description('Average response time')
                ->descriptionIcon('heroicon-m-clock')
                ->color($today->avg('latency_ms') > 3000 ? 'danger' : 'success'),

            Stat::make('Error Rate', round(($today->where('status_code', '>=', 400)->count() / max($today->count(), 1)) * 100, 1) . '%')
                ->description('Failed requests')
                ->descriptionIcon('heroicon-m-exclamation-triangle')
                ->color('warning'),

            Stat::make('Month Cost', '$' . number_format($thisMonth->sum('cost_usd'), 2))
                ->description('Total spend this month')
                ->descriptionIcon('heroicon-m-calendar')
                ->color('primary'),
        ];
    }
}
