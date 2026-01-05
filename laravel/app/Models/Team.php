<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Team extends Model
{
    protected $fillable = [
        'name',
        'slug',
        'daily_budget',
        'monthly_budget',
        'max_steps_per_run',
        'timeout_seconds',
        'is_active',
        'settings',
    ];

    protected $casts = [
        'daily_budget' => 'decimal:2',
        'monthly_budget' => 'decimal:2',
        'is_active' => 'boolean',
        'settings' => 'array',
    ];

    public function users(): HasMany
    {
        return $this->hasMany(User::class);
    }

    public function apiKeys(): HasMany
    {
        return $this->hasMany(ApiKey::class);
    }

    public function agentRuns(): HasMany
    {
        return $this->hasMany(AgentRun::class);
    }

    public function getTodaysCostAttribute(): float
    {
        return $this->agentRuns()
            ->whereDate('started_at', today())
            ->sum('total_cost');
    }

    public function getActiveRunsCountAttribute(): int
    {
        return $this->agentRuns()
            ->where('status', 'running')
            ->count();
    }
}
