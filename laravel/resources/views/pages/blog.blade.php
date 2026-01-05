@extends('layouts.public')

@section('title', 'Blog')
@section('description', 'AgentWall Blog - Insights on AI agent governance, cost control, and security.')

@php
$selectedCategory = request('category');
$selectedTag = request('tag');
@endphp

@section('content')
<!-- Hero -->
<section class="pt-12 pb-8 px-4 bg-white">
    <div class="max-w-5xl mx-auto text-center">
        <span class="text-wall-blue font-semibold text-sm uppercase tracking-wider">Blog</span>
        <h1 class="text-4xl font-extrabold mt-2 mb-4 text-darkest">Insights & Updates</h1>
        <p class="text-xl text-gray-600">AI agent governance, cost control, and security best practices.</p>
    </div>
</section>

<!-- Categories -->
<section class="py-6 px-4 bg-white border-b border-gray-200">
    <div class="max-w-5xl mx-auto">
        <div class="flex flex-wrap items-center justify-center gap-3">
            <a href="/blog" class="px-4 py-2 rounded-full text-sm font-medium transition {{ !$selectedCategory && !$selectedTag ? 'gradient-bg text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200' }}">
                All Posts
            </a>
            @foreach($categories as $slug => $cat)
            <a href="/blog?category={{ $slug }}" class="px-4 py-2 rounded-full text-sm font-medium transition {{ $selectedCategory === $slug ? 'gradient-bg text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200' }}">
                {{ $cat['name'] }}
            </a>
            @endforeach
        </div>
    </div>
</section>

<!-- Featured Posts -->
@if(!$selectedCategory && !$selectedTag && $featuredPosts->count() > 0)
<section class="py-12 px-4 bg-lighter">
    <div class="max-w-5xl mx-auto">
        <h2 class="text-2xl font-bold text-darkest mb-8">Featured Articles</h2>
        <div class="grid md:grid-cols-3 gap-6">
            @foreach($featuredPosts as $post)
            <a href="/blog/{{ $post->slug }}" class="group bg-white rounded-2xl border border-gray-200 overflow-hidden hover:shadow-xl transition-all duration-300">
                <div class="h-44 overflow-hidden">
                    <img src="{{ $post->image_url }}" alt="{{ $post->title }}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                </div>
                <div class="p-5">
                    <span class="text-xs font-semibold text-{{ $categories[$post->category]['color'] }} uppercase">{{ $categories[$post->category]['name'] }}</span>
                    <h3 class="font-bold text-darkest mt-2 mb-2 group-hover:text-wall-blue transition line-clamp-2">{{ $post->title }}</h3>
                    <p class="text-gray-600 text-sm line-clamp-2">{{ $post->excerpt }}</p>
                    <div class="mt-4 flex items-center text-xs text-gray-500">
                        <span>{{ $post->date->format('M d, Y') }}</span>
                        <span class="mx-2">•</span>
                        <span>{{ $post->read_time }} min read</span>
                    </div>
                </div>
            </a>
            @endforeach
        </div>
    </div>
</section>
@endif

<!-- All Posts -->
<section class="py-12 px-4 {{ !$selectedCategory && !$selectedTag ? 'bg-white' : 'bg-lighter' }}">
    <div class="max-w-5xl mx-auto">
        @if($selectedCategory || $selectedTag)
        <div class="mb-8 flex items-center gap-4">
            <h2 class="text-2xl font-bold text-darkest">
                @if($selectedCategory)
                    {{ $categories[$selectedCategory]['name'] }}
                @elseif($selectedTag)
                    Tag: {{ ucfirst(str_replace('-', ' ', $selectedTag)) }}
                @endif
            </h2>
            <a href="/blog" class="text-wall-blue text-sm hover:underline">← All posts</a>
        </div>
        @else
        <h2 class="text-2xl font-bold text-darkest mb-8">All Articles</h2>
        @endif
        
        <div class="grid md:grid-cols-2 gap-6">
            @foreach($posts as $post)
            <a href="/blog/{{ $post->slug }}" class="group bg-white rounded-2xl border border-gray-200 overflow-hidden hover:shadow-xl transition-all duration-300 flex">
                <div class="w-32 md:w-40 flex-shrink-0 overflow-hidden">
                    <img src="{{ $post->image_url }}" alt="{{ $post->title }}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                </div>
                <div class="p-5 flex-1">
                    <span class="text-xs font-semibold text-{{ $categories[$post->category]['color'] }} uppercase">{{ $categories[$post->category]['name'] }}</span>
                    <h3 class="font-bold text-darkest mt-1 mb-2 group-hover:text-wall-blue transition line-clamp-2">{{ $post->title }}</h3>
                    <p class="text-gray-600 text-sm line-clamp-2 hidden md:block">{{ $post->excerpt }}</p>
                    <div class="mt-3 flex items-center text-xs text-gray-500">
                        <span>{{ $post->date->format('M d, Y') }}</span>
                        <span class="mx-2">•</span>
                        <span>{{ $post->read_time }} min</span>
                    </div>
                </div>
            </a>
            @endforeach
        </div>
    </div>
</section>

<!-- Newsletter -->
<section class="py-16 px-4 bg-darkest">
    <div class="max-w-2xl mx-auto text-center" x-data="{ email: '', subscribed: false }">
        <h2 class="text-2xl font-bold text-white mb-4">Stay Updated</h2>
        <p class="text-gray-400 mb-6">Get the latest insights on AI agent governance delivered to your inbox.</p>
        <form @submit.prevent="subscribed = true" x-show="!subscribed" class="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
            <input type="email" x-model="email" placeholder="your@email.com" required class="flex-1 px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:border-wall-blue">
            <button type="submit" class="gradient-bg hover:opacity-90 text-white px-6 py-3 rounded-xl font-semibold transition">Subscribe</button>
        </form>
        <div x-show="subscribed" x-transition class="text-success-green font-medium">✓ You're subscribed!</div>
    </div>
</section>
@endsection
