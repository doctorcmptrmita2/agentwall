<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\RequestLogController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Internal API routes for FastAPI -> Laravel communication
|
*/

Route::prefix('internal')->group(function () {
    Route::post('/logs', [RequestLogController::class, 'store']);
    Route::post('/logs/bulk', [RequestLogController::class, 'bulkStore']);
});
