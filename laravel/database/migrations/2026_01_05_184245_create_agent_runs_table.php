<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        // Note: This table is for caching/quick access
        // Full logs are in ClickHouse
        Schema::create('agent_runs', function (Blueprint $table) {
            $table->id();
            $table->string('run_id', 36)->unique();
            $table->foreignId('team_id')->constrained()->cascadeOnDelete();
            $table->foreignId('api_key_id')->nullable()->constrained()->nullOnDelete();
            $table->string('agent_id')->nullable();
            $table->string('agent_name')->nullable();
            $table->string('model')->nullable();
            $table->integer('step_count')->default(0);
            $table->integer('total_tokens')->default(0);
            $table->decimal('total_cost', 10, 6)->default(0);
            $table->integer('total_latency_ms')->default(0);
            $table->enum('status', ['running', 'completed', 'failed', 'killed'])->default('running');
            $table->string('kill_reason')->nullable();
            $table->boolean('loop_detected')->default(false);
            $table->boolean('budget_exceeded')->default(false);
            $table->timestamp('started_at');
            $table->timestamp('ended_at')->nullable();
            $table->json('metadata')->nullable();
            $table->timestamps();
            
            $table->index(['team_id', 'status']);
            $table->index(['team_id', 'started_at']);
            $table->index('run_id');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('agent_runs');
    }
};
