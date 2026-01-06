<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Str;

class AgentRun extends Model
{
    protected $fillable = [
        'run_id',
        'team_id',
        'api_key_id',
        'agent_id',
        'agent_name',
        'model',
        'step_count',
        'total_tokens',
        'total_cost',
        'total_latency_ms',
        'status',
        'kill_reason',
        'loop_detected',
        'budget_exceeded',
        'started_at',
        'ended_at',
        'metadata',
    ];

    protected static function boot()
    {
        parent::boot();

        static::creating(function ($model) {
            if (!$model->run_id) {
                $model->run_id = 'run_' . Str::uuid();
            }
            if (!$model->started_at) {
                $model->started_at = now();
            }
        });
    }

    protected $casts = [
        'total_cost' => 'decimal:6',
        'loop_detected' => 'boolean',
        'budget_exceeded' => 'boolean',
        'started_at' => 'datetime',
        'ended_at' => 'datetime',
        'metadata' => 'array',
    ];

    public function team(): BelongsTo
    {
        return $this->belongsTo(Team::class);
    }

    public function apiKey(): BelongsTo
    {
        return $this->belongsTo(ApiKey::class);
    }

    public function getDurationAttribute(): ?int
    {
        if (!$this->ended_at) {
            return now()->diffInSeconds($this->started_at);
        }
        return $this->ended_at->diffInSeconds($this->started_at);
    }

    public function getStatusColorAttribute(): string
    {
        return match($this->status) {
            'running' => 'warning',
            'completed' => 'success',
            'failed' => 'danger',
            'killed' => 'danger',
            default => 'gray',
        };
    }

    public function scopeRunning($query)
    {
        return $query->where('status', 'running');
    }

    public function scopeToday($query)
    {
        return $query->whereDate('started_at', today());
    }
}
