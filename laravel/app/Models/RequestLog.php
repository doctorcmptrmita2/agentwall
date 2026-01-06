<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class RequestLog extends Model
{
    public $timestamps = false;
    
    protected $fillable = [
        'request_id',
        'run_id',
        'team_id',
        'user_id',
        'api_key_id',
        'model',
        'provider',
        'endpoint',
        'stream',
        'prompt_tokens',
        'completion_tokens',
        'total_tokens',
        'cost_usd',
        'latency_ms',
        'ttfb_ms',
        'status_code',
        'error_type',
        'error_message',
        'dlp_triggered',
        'loop_detected',
        'budget_exceeded',
        'ip_address',
        'user_agent',
        'created_at',
    ];

    protected $casts = [
        'stream' => 'boolean',
        'dlp_triggered' => 'boolean',
        'loop_detected' => 'boolean',
        'budget_exceeded' => 'boolean',
        'cost_usd' => 'decimal:8',
        'created_at' => 'datetime',
    ];

    public function team(): BelongsTo
    {
        return $this->belongsTo(Team::class);
    }

    public function agentRun(): BelongsTo
    {
        return $this->belongsTo(AgentRun::class, 'run_id', 'run_id');
    }

    public function getStatusColorAttribute(): string
    {
        return match(true) {
            $this->status_code >= 500 => 'danger',
            $this->status_code >= 400 => 'warning',
            $this->status_code >= 200 && $this->status_code < 300 => 'success',
            default => 'gray',
        };
    }

    public function getProviderColorAttribute(): string
    {
        return match($this->provider) {
            'openai' => 'success',
            'openrouter' => 'info',
            'groq' => 'warning',
            'deepseek' => 'primary',
            'mistral' => 'danger',
            'ollama' => 'gray',
            default => 'gray',
        };
    }

    // Scopes
    public function scopeSuccessful($query)
    {
        return $query->where('status_code', '>=', 200)->where('status_code', '<', 300);
    }

    public function scopeFailed($query)
    {
        return $query->where('status_code', '>=', 400);
    }

    public function scopeToday($query)
    {
        return $query->whereDate('created_at', today());
    }

    public function scopeThisMonth($query)
    {
        return $query->whereMonth('created_at', now()->month)
                     ->whereYear('created_at', now()->year);
    }
}
