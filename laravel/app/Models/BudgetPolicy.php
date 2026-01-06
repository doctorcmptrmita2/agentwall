<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class BudgetPolicy extends Model
{
    protected $fillable = [
        'team_id',
        'name',
        'description',
        'daily_limit',
        'monthly_limit',
        'per_run_limit',
        'alert_threshold',
        'auto_kill_enabled',
        'is_active',
    ];

    protected $casts = [
        'daily_limit' => 'decimal:6',
        'monthly_limit' => 'decimal:6',
        'per_run_limit' => 'decimal:6',
        'alert_threshold' => 'decimal:6',
        'auto_kill_enabled' => 'boolean',
        'is_active' => 'boolean',
    ];

    public function team(): BelongsTo
    {
        return $this->belongsTo(Team::class);
    }

    /**
     * Check if run exceeds per-run budget
     */
    public function exceedsPerRunBudget(float $cost): bool
    {
        return $cost > (float)$this->per_run_limit;
    }

    /**
     * Check if daily budget exceeded
     */
    public function exceedsDailyBudget(float $todaySpent): bool
    {
        return $todaySpent > (float)$this->daily_limit;
    }

    /**
     * Check if monthly budget exceeded
     */
    public function exceedsMonthlyBudget(float $monthSpent): bool
    {
        return $monthSpent > (float)$this->monthly_limit;
    }

    /**
     * Check if should alert
     */
    public function shouldAlert(float $cost): bool
    {
        return $cost > (float)$this->alert_threshold;
    }
}
