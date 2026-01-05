@extends('layouts.public')

@section('title', $post['title'] . ' | AgentWall Blog')
@section('description', $post['excerpt'])

@php
$category = $categories[$post->category];
preg_match_all('/<h2[^>]*>(.*?)<\/h2>/i', $post->content ?? '', $headings);
$toc = $headings[1] ?? [];
@endphp

@section('content')
<nav class="pt-6 px-4 bg-white">
    <div class="max-w-4xl mx-auto">
        <ol class="flex items-center gap-2 text-sm text-gray-500">
            <li><a href="/" class="hover:text-wall-blue">Home</a></li>
            <li>/</li>
            <li><a href="/blog" class="hover:text-wall-blue">Blog</a></li>
            <li>/</li>
            <li class="text-darkest font-medium truncate max-w-xs">{{ $post['title'] }}</li>
        </ol>
    </div>
</nav>

<header class="pt-8 pb-6 px-4 bg-white">
    <div class="max-w-4xl mx-auto">
        <span class="inline-block px-3 py-1 rounded-full text-sm font-semibold mb-4 bg-wall-blue/10 text-wall-blue">
            {{ $category['name'] }}
        </span>
        <h1 class="text-3xl md:text-4xl font-extrabold text-darkest mb-6">{{ $post->title }}</h1>
        <p class="text-xl text-gray-600 mb-8">{{ $post->excerpt }}</p>
        <div class="flex items-center gap-6 pb-8 border-b border-gray-200">
            <div class="flex items-center gap-3">
                <div class="w-12 h-12 rounded-full gradient-bg flex items-center justify-center text-white font-bold">
                    {{ substr($post->author, 0, 1) }}
                </div>
                <div>
                    <div class="font-semibold text-darkest">{{ $post->author }}</div>
                    <div class="text-sm text-gray-500">AgentWall Team</div>
                </div>
            </div>
            <div class="flex items-center gap-4 text-sm text-gray-500">
                <span>{{ $post->date->format('M d, Y') }}</span>
                <span>•</span>
                <span>{{ $post->read_time }} min read</span>
            </div>
        </div>
    </div>
</header>

<section class="px-4 py-8 bg-white">
    <div class="max-w-4xl mx-auto">
        <img src="{{ $post->image_url }}" alt="{{ $post->title }}" class="w-full h-64 md:h-96 object-cover rounded-2xl shadow-lg">
        <p class="text-center text-sm text-gray-500 mt-3">Photo by Unsplash</p>
    </div>
</section>

<section class="py-8 px-4 bg-white">
    <div class="max-w-6xl mx-auto grid lg:grid-cols-4 gap-12">
        <aside class="lg:col-span-1 order-2 lg:order-1">
            <div class="lg:sticky lg:top-24">
                @if(count($toc) > 0)
                <nav class="bg-lighter rounded-2xl p-6 mb-6">
                    <h2 class="font-bold text-darkest mb-4">Contents</h2>
                    <ol class="space-y-2 text-sm">
                        @foreach($toc as $i => $h)
                        <li>
                            <a href="#section-{{ $i + 1 }}" class="text-gray-600 hover:text-wall-blue">
                                {{ $i + 1 }}. {{ strip_tags($h) }}
                            </a>
                        </li>
                        @endforeach
                    </ol>
                </nav>
                @endif
                <div class="bg-lighter rounded-2xl p-6">
                    <h2 class="font-bold text-darkest mb-4">Tags</h2>
                    <div class="flex flex-wrap gap-2">
                        @foreach($post->tags as $tag)
                        <span class="px-3 py-1 bg-white border rounded-full text-sm text-gray-600">#{{ $tag }}</span>
                        @endforeach
                    </div>
                </div>
            </div>
        </aside>
        
        <article class="lg:col-span-3 order-1 lg:order-2">
            <div class="prose prose-lg max-w-none">
                @php
                $counter = 0;
                $contentWithIds = preg_replace_callback('/<h2([^>]*)>(.*?)<\/h2>/i', function($m) use (&$counter) {
                    $counter++;
                    return '<h2' . $m[1] . ' id="section-' . $counter . '" class="text-2xl font-bold text-darkest mt-12 mb-4 pb-2 border-b border-gray-200">' . $m[2] . '</h2>';
                }, $post->content ?? '<p>Content coming soon...</p>');
                @endphp
                {!! $contentWithIds !!}
            </div>
            
            <!-- FAQ Section -->
            @if($post->faqs && count($post->faqs) > 0)
            <div class="mt-12 pt-8 border-t border-gray-200" id="faq-section">
                <h2 class="text-2xl font-bold text-darkest mb-6 flex items-center gap-3">
                    <span class="w-10 h-10 bg-wall-blue/10 rounded-xl flex items-center justify-center">
                        <svg class="w-5 h-5 text-wall-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </span>
                    Frequently Asked Questions
                </h2>
                
                <div class="space-y-3" x-data="{ open: 0 }">
                    @foreach($post->faqs as $index => $faq)
                    <div class="border border-gray-200 rounded-xl overflow-hidden">
                        <button type="button" @click="open = open === {{ $index + 1 }} ? 0 : {{ $index + 1 }}" class="w-full px-6 py-4 text-left flex items-center justify-between bg-white hover:bg-gray-50 transition">
                            <span class="font-semibold text-darkest">{{ $faq['q'] }}</span>
                            <svg class="w-5 h-5 text-gray-400 transition-transform duration-200" :class="open === {{ $index + 1 }} && 'rotate-180'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                            </svg>
                        </button>
                        <div x-show="open === {{ $index + 1 }}" x-transition class="px-6 pb-4 bg-gray-50 border-t border-gray-100">
                            <p class="text-gray-600 pt-4">{{ $faq['a'] }}</p>
                        </div>
                    </div>
                    @endforeach
                </div>
            </div>
            @endif
        </article>
    </div>
</section>

<section class="py-8 px-4 bg-white border-t border-gray-100">
    <div class="max-w-4xl mx-auto">
        <div class="bg-lighter rounded-2xl p-8 flex gap-6">
            <div class="w-20 h-20 rounded-2xl gradient-bg flex items-center justify-center text-white font-bold text-2xl">
                {{ substr($post->author, 0, 1) }}
            </div>
            <div>
                <div class="text-sm text-wall-blue font-semibold mb-1">Written by</div>
                <h3 class="text-xl font-bold text-darkest mb-2">{{ $post->author }}</h3>
                <p class="text-gray-600">Security researcher and AI governance expert at AgentWall.</p>
            </div>
        </div>
    </div>
</section>

<section class="py-12 px-4 bg-lighter">
    <div class="max-w-4xl mx-auto">
        <div class="gradient-bg rounded-2xl p-8 md:p-12 text-center text-white">
            <h2 class="text-2xl md:text-3xl font-bold mb-4">Ready to protect your AI agents?</h2>
            <p class="text-white/80 mb-8">Start using AgentWall today. No credit card required.</p>
            <a href="/contact" class="inline-block bg-white text-wall-blue px-8 py-4 rounded-xl font-semibold hover:bg-gray-100 transition">
                Get Started Free →
            </a>
        </div>
    </div>
</section>

@if($relatedPosts->count() > 0)
<section class="py-12 px-4 bg-white">
    <div class="max-w-5xl mx-auto">
        <h2 class="text-2xl font-bold text-darkest mb-8">Related Articles</h2>
        <div class="grid md:grid-cols-3 gap-6">
            @foreach($relatedPosts as $r)
            <a href="/blog/{{ $r->slug }}" class="bg-lighter rounded-2xl p-5 hover:shadow-lg transition">
                <span class="text-xs font-semibold text-wall-blue uppercase">{{ $categories[$r->category]['name'] }}</span>
                <h3 class="font-bold text-darkest mt-2 mb-2 line-clamp-2">{{ $r->title }}</h3>
                <span class="text-xs text-gray-500">{{ $r->read_time }} min read</span>
            </a>
            @endforeach
        </div>
    </div>
</section>
@endif
@endsection
