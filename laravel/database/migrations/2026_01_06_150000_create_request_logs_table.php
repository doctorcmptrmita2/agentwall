<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('request_logs', function (Blueprint $table) {
            $table->id();
            $table->string('request_id', 50)->unique();
            $table->string('run_id', 50)->nullable()->index();
            $table->unsignedBigInteger('team_id')->nullable()->index();
            $table->unsignedBigInteger('user_id')->nullable();
            $table->string('api_key_id', 50)->nullable();
            
            // Request details
            $table->string('model', 100);
            $table->string('provider', 50)->default('openai');
            $table->string('endpoint', 100)->default('/v1/chat/completions');
            $table->boolean('stream')->default(false);
            
            // Tokens & Cost
            $table->integer('prompt_tokens')->default(0);
            $table->integer('completion_tokens')->default(0);
            $table->integer('total_tokens')->default(0);
            $table->decimal('cost_usd', 12, 8)->default(0);
            
            // Performance
            $table->integer('latency_ms')->default(0);
            $table->integer('ttfb_ms')->nullable(); // Time to first byte (streaming)
            
            // Status
            $table->integer('status_code')->default(200);
            $table->string('error_type')->nullable();
            $table->text('error_message')->nullable();
            
            // Security flags
            $table->boolean('dlp_triggered')->default(false);
            $table->boolean('loop_detected')->default(false);
            $table->boolean('budget_exceeded')->default(false);
            
            // Metadata
            $table->string('ip_address', 45)->nullable();
            $table->string('user_agent', 255)->nullable();
            
            $table->timestamp('created_at')->useCurrent();
            
            // Indexes for common queries
            $table->index(['team_id', 'created_at']);
            $table->index(['model', 'created_at']);
            $table->index(['provider', 'created_at']);
            $table->index('created_at');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('request_logs');
    }
};
