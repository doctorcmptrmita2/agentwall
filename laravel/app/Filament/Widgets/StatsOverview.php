<?php

namespace App\Filament\Widgets;

use App\Models\AgentRun;
use App\Models\ApiKey;
use Filament\Widgets\StatsOverviewWidget as BaseWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class StatsOverview extends BaseWidget
{
    protected static ?int $sort = 1;
    
    protected function getStats(): array
    {
        $todayRuns = AgentRun::today();
        $activeRuns = AgentRun::running()->count();
        $todayCost = AgentRun::today()->sum('total_cost');
        $todayRequests = AgentRun::today()->count();
        $activeKeys = ApiKey::where('is_active', true)->count();
        
        // Get killed runs today
        $killedToday = AgentRun::today()
            ->where('status', 'killed')
            ->count();
        
        // Get loop detections today
        $loopsToday = AgentRun::today()
            ->where('loop_detected', true)
            ->count();

        return [
            Stat::make('Active Runs', $activeRuns)
                ->description('Currently running agents')
                ->descriptionIcon('heroicon-m-play')
                ->color($activeRuns > 10 ? 'warning' : 'success')
                ->chart([7, 3, 4, 5, 6, $activeRuns]),
                
            Stat::make('Today\'s Cost', '$' . number_format($todayCost, 4))
                ->description('Total spend today')
                ->descriptionIcon('heroicon-m-currency-dollar')
                ->color('primary'),
                
            Stat::make('Today\'s Requests', $todayRequests)
                ->description('API calls today')
                ->descriptionIcon('heroicon-m-arrow-trending-up')
                ->color('info'),
                
            Stat::make('Killed Runs', $killedToday)
                ->description('Auto-stopped today')
                ->descriptionIcon('heroicon-m-stop')
                ->color($killedToday > 0 ? 'danger' : 'success'),
                
            Stat::make('Loop Detections', $loopsToday)
                ->description('Infinite loops caught')
                ->descriptionIcon('heroicon-m-arrow-path')
                ->color($loopsToday > 0 ? 'warning' : 'success'),
                
            Stat::make('Active API Keys', $activeKeys)
                ->description('Keys in use')
                ->descriptionIcon('heroicon-m-key')
                ->color('gray'),
        ];
    }
}
