<?php

namespace App\Data;

class BlogContent
{
    public static function getContent(string $slug): string
    {
        $contents = self::getAllContent();
        
        // Eğer içerik varsa döndür
        if (isset($contents[$slug])) {
            return $contents[$slug];
        }
        
        // Yoksa Article'dan başlık ve excerpt'i al, dinamik içerik oluştur
        $article = \App\Models\Article::where('slug', $slug)->first();
        if (!$article) {
            return '<p class="text-gray-600">Content not found.</p>';
        }
        
        return self::generateDefaultContent($article);
    }
    
    private static function generateDefaultContent($article): string
    {
        $title = $article->title;
        $excerpt = $article->excerpt;
        
        return <<<HTML
<p class="text-xl text-gray-600 leading-relaxed mb-8">{$excerpt}</p>

<h2>Overview</h2>
<p>This article explores the key concepts and best practices related to {$title}.</p>

<h2>Key Challenges</h2>
<ul class="list-disc pl-6 space-y-2 my-4">
    <li><strong>Security Risks:</strong> Protecting against unauthorized access</li>
    <li><strong>Cost Management:</strong> Preventing runaway spending</li>
    <li><strong>Operational Visibility:</strong> Real-time monitoring</li>
</ul>

<h2>Best Practices</h2>
<p>Implement comprehensive governance frameworks with AgentWall.</p>

<p class="mt-8 p-6 bg-lighter rounded-xl">
    <strong>Ready to secure your AI agents?</strong> <a href="/contact" class="text-wall-blue hover:underline">Get started</a>.
</p>
HTML;
    }


    private static function getAllContent(): array
    {
        return [];
    }
}
