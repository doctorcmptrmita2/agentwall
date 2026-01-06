<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\RequestLog;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class RequestLogController extends Controller
{
    public function store(Request $request): JsonResponse
    {
        // Validate internal secret
        $secret = $request->header('X-Internal-Secret');
        if ($secret !== config('services.agentwall.internal_secret')) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }

        $validated = $request->validate([
            'request_id' => 'required|string|max:50',
            'run_id' => 'nullable|string|max:50',
            'team_id' => 'nullable|integer',
            'user_id' => 'nullable|integer',
            'api_key_id' => 'nullable|string|max:50',
            'model' => 'required|string|max:100',
            'provider' => 'nullable|string|max:50',
            'endpoint' => 'nullable|string|max:100',
            'stream' => 'nullable|boolean',
            'prompt_tokens' => 'nullable|integer',
            'completion_tokens' => 'nullable|integer',
            'total_tokens' => 'nullable|integer',
            'cost_usd' => 'nullable|numeric',
            'latency_ms' => 'nullable|integer',
            'ttfb_ms' => 'nullable|integer',
            'status_code' => 'nullable|integer',
            'error_type' => 'nullable|string',
            'error_message' => 'nullable|string',
            'dlp_triggered' => 'nullable|boolean',
            'loop_detected' => 'nullable|boolean',
            'budget_exceeded' => 'nullable|boolean',
            'ip_address' => 'nullable|string|max:45',
            'user_agent' => 'nullable|string|max:255',
        ]);

        $log = RequestLog::create($validated);

        return response()->json([
            'success' => true,
            'id' => $log->id,
        ], 201);
    }

    public function bulkStore(Request $request): JsonResponse
    {
        $secret = $request->header('X-Internal-Secret');
        if ($secret !== config('services.agentwall.internal_secret')) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }

        $logs = $request->input('logs', []);
        $inserted = 0;

        foreach ($logs as $logData) {
            try {
                RequestLog::create($logData);
                $inserted++;
            } catch (\Exception $e) {
                // Skip invalid logs
            }
        }

        return response()->json([
            'success' => true,
            'inserted' => $inserted,
        ], 201);
    }
}
