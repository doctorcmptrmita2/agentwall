<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    protected $fillable = [
        'slug',
        'title',
        'excerpt',
        'image_url',
        'content',
        'faqs',
        'category',
        'tags',
        'author',
        'date',
        'read_time',
        'featured',
    ];

    protected $casts = [
        'tags' => 'array',
        'faqs' => 'array',
        'date' => 'date',
        'featured' => 'boolean',
    ];
}
