<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('api_keys', function (Blueprint $table) {
            $table->id();
            $table->foreignId('team_id')->constrained()->cascadeOnDelete();
            $table->foreignId('user_id')->nullable()->constrained()->nullOnDelete();
            $table->string('name');
            $table->string('key_prefix', 12); // First 12 chars for display (aw-xxxx...)
            $table->string('key_hash', 64)->unique(); // SHA256 hash of full key
            $table->decimal('daily_budget', 10, 2)->nullable(); // Override team budget
            $table->decimal('spent_today', 10, 4)->default(0);
            $table->integer('requests_today')->default(0);
            $table->integer('max_steps_per_run')->nullable(); // Override team setting
            $table->timestamp('last_used_at')->nullable();
            $table->timestamp('expires_at')->nullable();
            $table->boolean('is_active')->default(true);
            $table->json('allowed_models')->nullable(); // ["gpt-4o", "gpt-4o-mini"]
            $table->json('metadata')->nullable();
            $table->timestamps();
            
            $table->index(['team_id', 'is_active']);
            $table->index('key_hash');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('api_keys');
    }
};
