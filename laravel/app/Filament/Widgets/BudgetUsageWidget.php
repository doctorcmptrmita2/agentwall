<?php

namespace App\Filament\Widgets;

use App\Models\AgentRun;
use App\Models\BudgetPolicy;
use Filament\Widgets\StatsOverviewWidget as BaseWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class BudgetUsageWidget extends BaseWidget
{
    protected static ?int $sort = 2;
    protected static ?string $pollingInterval = '30s';

    protected function getStats(): array
    {
        // Get active budget policy (first one for now)
        $policy = BudgetPolicy::where('is_active', true)->first();
        
        if (!$policy) {
            return [
                Stat::make('Budget Policy', 'Not Configured')
                    ->description('Create a budget policy to track spending')
                    ->descriptionIcon('heroicon-m-exclamation-triangle')
                    ->color('warning'),
            ];
        }

        // Calculate spending
        $todaySpent = AgentRun::today()->sum('total_cost');
        $monthSpent = AgentRun::whereMonth('started_at', now()->month)
            ->whereYear('started_at', now()->year)
            ->sum('total_cost');

        // Calculate percentages
        $dailyPercent = $policy->daily_limit > 0 
            ? min(100, ($todaySpent / $policy->daily_limit) * 100) 
            : 0;
        $monthlyPercent = $policy->monthly_limit > 0 
            ? min(100, ($monthSpent / $policy->monthly_limit) * 100) 
            : 0;

        // Determine colors based on usage
        $dailyColor = match(true) {
            $dailyPercent >= 90 => 'danger',
            $dailyPercent >= 70 => 'warning',
            default => 'success',
        };
        $monthlyColor = match(true) {
            $monthlyPercent >= 90 => 'danger',
            $monthlyPercent >= 70 => 'warning',
            default => 'success',
        };

        return [
            Stat::make('Daily Budget', '$' . number_format($todaySpent, 2) . ' / $' . number_format($policy->daily_limit, 2))
                ->description(number_format($dailyPercent, 1) . '% used today')
                ->descriptionIcon('heroicon-m-calendar')
                ->color($dailyColor)
                ->chart($this->getDailyChart()),

            Stat::make('Monthly Budget', '$' . number_format($monthSpent, 2) . ' / $' . number_format($policy->monthly_limit, 2))
                ->description(number_format($monthlyPercent, 1) . '% used this month')
                ->descriptionIcon('heroicon-m-calendar-days')
                ->color($monthlyColor)
                ->chart($this->getMonthlyChart()),

            Stat::make('Per-Run Limit', '$' . number_format($policy->per_run_limit, 2))
                ->description($policy->auto_kill_enabled ? 'Auto-kill enabled' : 'Auto-kill disabled')
                ->descriptionIcon($policy->auto_kill_enabled ? 'heroicon-m-stop' : 'heroicon-m-minus')
                ->color($policy->auto_kill_enabled ? 'danger' : 'gray'),

            Stat::make('Daily Remaining', '$' . number_format(max(0, $policy->daily_limit - $todaySpent), 2))
                ->description('Available today')
                ->descriptionIcon('heroicon-m-banknotes')
                ->color($dailyColor),
        ];
    }

    private function getDailyChart(): array
    {
        // Get last 7 days spending
        $data = [];
        for ($i = 6; $i >= 0; $i--) {
            $date = now()->subDays($i);
            $spent = AgentRun::whereDate('started_at', $date)->sum('total_cost');
            $data[] = (float)$spent;
        }
        return $data;
    }

    private function getMonthlyChart(): array
    {
        // Get last 6 months spending
        $data = [];
        for ($i = 5; $i >= 0; $i--) {
            $date = now()->subMonths($i);
            $spent = AgentRun::whereMonth('started_at', $date->month)
                ->whereYear('started_at', $date->year)
                ->sum('total_cost');
            $data[] = (float)$spent;
        }
        return $data;
    }
}
