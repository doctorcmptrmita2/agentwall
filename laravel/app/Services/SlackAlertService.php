<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class SlackAlertService
{
    private string $webhookUrl;
    private bool $enabled;

    public function __construct()
    {
        $this->webhookUrl = config('services.slack.webhook_url', '');
        $this->enabled = config('services.slack.enabled', false);
    }

    /**
     * Send alert to Slack
     */
    public function alert(string $title, string $message, string $color = '#FF6B6B', array $fields = []): bool
    {
        if (!$this->enabled || !$this->webhookUrl) {
            Log::debug('Slack alerts disabled or webhook not configured');
            return false;
        }

        try {
            $payload = [
                'attachments' => [
                    [
                        'color' => $color,
                        'title' => $title,
                        'text' => $message,
                        'fields' => $fields,
                        'ts' => now()->timestamp,
                    ]
                ]
            ];

            $response = Http::post($this->webhookUrl, $payload);

            if (!$response->successful()) {
                Log::error('Slack alert failed', [
                    'status' => $response->status(),
                    'body' => $response->body()
                ]);
                return false;
            }

            return true;
        } catch (\Exception $e) {
            Log::error('Slack alert exception', ['error' => $e->getMessage()]);
            return false;
        }
    }

    /**
     * Alert: Run killed
     */
    public function runKilled(string $runId, string $reason, float $cost): bool
    {
        return $this->alert(
            '🛑 Agent Run Killed',
            "Run `$runId` was terminated",
            '#FF6B6B',
            [
                ['title' => 'Reason', 'value' => $reason, 'short' => true],
                ['title' => 'Cost', 'value' => '$' . number_format($cost, 4), 'short' => true],
            ]
        );
    }

    /**
     * Alert: Loop detected
     */
    public function loopDetected(string $runId, int $stepCount, float $cost): bool
    {
        return $this->alert(
            '🔄 Infinite Loop Detected',
            "Run `$runId` detected infinite loop pattern",
            '#FFA500',
            [
                ['title' => 'Steps', 'value' => (string)$stepCount, 'short' => true],
                ['title' => 'Cost', 'value' => '$' . number_format($cost, 4), 'short' => true],
            ]
        );
    }

    /**
     * Alert: Budget exceeded
     */
    public function budgetExceeded(string $runId, float $spent, float $budget): bool
    {
        return $this->alert(
            '💰 Budget Exceeded',
            "Run `$runId` exceeded budget limit",
            '#FF6B6B',
            [
                ['title' => 'Spent', 'value' => '$' . number_format($spent, 4), 'short' => true],
                ['title' => 'Budget', 'value' => '$' . number_format($budget, 4), 'short' => true],
            ]
        );
    }

    /**
     * Alert: Run completed
     */
    public function runCompleted(string $runId, int $steps, float $cost, int $latencyMs): bool
    {
        return $this->alert(
            '✅ Agent Run Completed',
            "Run `$runId` finished successfully",
            '#51CF66',
            [
                ['title' => 'Steps', 'value' => (string)$steps, 'short' => true],
                ['title' => 'Cost', 'value' => '$' . number_format($cost, 4), 'short' => true],
                ['title' => 'Latency', 'value' => $latencyMs . 'ms', 'short' => true],
            ]
        );
    }

    /**
     * Alert: Run failed
     */
    public function runFailed(string $runId, string $error): bool
    {
        return $this->alert(
            '❌ Agent Run Failed',
            "Run `$runId` encountered an error",
            '#FF6B6B',
            [
                ['title' => 'Error', 'value' => $error, 'short' => false],
            ]
        );
    }
}
