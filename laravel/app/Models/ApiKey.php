<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Str;

class ApiKey extends Model
{
    protected $fillable = [
        'team_id',
        'user_id',
        'name',
        'key_prefix',
        'key_hash',
        'daily_budget',
        'spent_today',
        'requests_today',
        'max_steps_per_run',
        'last_used_at',
        'expires_at',
        'is_active',
        'allowed_models',
        'metadata',
    ];

    protected $casts = [
        'daily_budget' => 'decimal:2',
        'spent_today' => 'decimal:4',
        'is_active' => 'boolean',
        'last_used_at' => 'datetime',
        'expires_at' => 'datetime',
        'allowed_models' => 'array',
        'metadata' => 'array',
    ];

    protected $hidden = [
        'key_hash',
    ];

    public function team(): BelongsTo
    {
        return $this->belongsTo(Team::class);
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function agentRuns(): HasMany
    {
        return $this->hasMany(AgentRun::class);
    }

    /**
     * Generate a new API key
     * Returns the plain key (only shown once!)
     */
    public static function generateKey(): array
    {
        $key = 'aw-' . Str::random(32);
        
        return [
            'key' => $key,
            'prefix' => substr($key, 0, 12),
            'hash' => hash('sha256', $key),
        ];
    }

    /**
     * Verify a key against this record
     */
    public function verifyKey(string $key): bool
    {
        return hash('sha256', $key) === $this->key_hash;
    }

    /**
     * Check if key is valid (active, not expired, within budget)
     */
    public function isValid(): bool
    {
        if (!$this->is_active) {
            return false;
        }

        if ($this->expires_at && $this->expires_at->isPast()) {
            return false;
        }

        if ($this->daily_budget && $this->spent_today >= $this->daily_budget) {
            return false;
        }

        return true;
    }

    public function getMaskedKeyAttribute(): string
    {
        return $this->key_prefix . '...' . str_repeat('*', 8);
    }
}
