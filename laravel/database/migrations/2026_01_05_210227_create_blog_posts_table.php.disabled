<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('blog_posts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('blog_category_id')->constrained()->cascadeOnDelete();
            $table->string('slug')->unique();
            $table->string('title');
            $table->text('excerpt');
            $table->longText('content');
            $table->string('author')->default('AgentWall Team');
            $table->date('published_at');
            $table->integer('read_time')->default(5);
            $table->boolean('featured')->default(false);
            $table->boolean('published')->default(true);
            $table->string('featured_image')->nullable();
            $table->string('meta_title')->nullable();
            $table->string('meta_description')->nullable();
            $table->integer('views')->default(0);
            $table->timestamps();
            
            $table->index('slug');
            $table->index('published_at');
            $table->index(['published', 'featured']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('blog_posts');
    }
};
