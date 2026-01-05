<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class BlogPost extends Model
{
    protected $fillable = [
        'blog_category_id',
        'slug',
        'title',
        'excerpt',
        'content',
        'author',
        'published_at',
        'read_time',
        'featured',
        'published',
        'featured_image',
        'meta_title',
        'meta_description',
        'views',
    ];

    protected $casts = [
        'published_at' => 'date',
        'featured' => 'boolean',
        'published' => 'boolean',
    ];

    public function category()
    {
        return $this->belongsTo(BlogCategory::class, 'blog_category_id');
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(BlogTag::class);
    }

    public function faqs(): HasMany
    {
        return $this->hasMany(BlogFaq::class)->orderBy('order');
    }

    public function scopePublished($query)
    {
        return $query->where('published', true);
    }

    public function scopeFeatured($query)
    {
        return $query->where('featured', true);
    }

    public function incrementViews()
    {
        $this->increment('views');
    }
}
