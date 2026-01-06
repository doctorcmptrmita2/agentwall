<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('budget_policies', function (Blueprint $table) {
            $table->id();
            $table->foreignId('team_id')->constrained()->onDelete('cascade');
            $table->string('name');
            $table->text('description')->nullable();
            
            // Budget limits
            $table->decimal('daily_limit', 10, 6)->default(100); // $100/day
            $table->decimal('monthly_limit', 10, 6)->default(3000); // $3000/month
            $table->decimal('per_run_limit', 10, 6)->default(10); // $10/run
            
            // Alert threshold (% of limit)
            $table->decimal('alert_threshold', 10, 6)->default(5); // Alert at $5
            
            // Auto-kill when exceeded
            $table->boolean('auto_kill_enabled')->default(true);
            $table->boolean('is_active')->default(true);
            
            $table->timestamps();
            $table->index(['team_id', 'is_active']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('budget_policies');
    }
};
