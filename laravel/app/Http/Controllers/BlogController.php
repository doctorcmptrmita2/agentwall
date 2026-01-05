<?php

namespace App\Http\Controllers;

use App\Models\Article;
use App\Data\BlogPosts;
use Illuminate\Http\Request;

class BlogController extends Controller
{
    public function index(Request $request)
    {
        $query = Article::query();
        
        if ($category = $request->get('category')) {
            $query->where('category', $category);
        }
        
        if ($tag = $request->get('tag')) {
            $query->whereJsonContains('tags', $tag);
        }
        
        $posts = $query->orderBy('date', 'desc')->get();
        $categories = BlogPosts::getCategories();
        $featuredPosts = Article::where('featured', true)
            ->orderBy('date', 'desc')
            ->limit(3)
            ->get();
        
        return view('pages.blog', compact('posts', 'categories', 'featuredPosts'));
    }
    
    public function show(string $slug)
    {
        $post = Article::where('slug', $slug)->firstOrFail();
        $categories = BlogPosts::getCategories();
        
        $relatedPosts = Article::where('category', $post->category)
            ->where('slug', '!=', $post->slug)
            ->orderBy('date', 'desc')
            ->limit(3)
            ->get();
        
        return view('pages.blog-post', compact('post', 'categories', 'relatedPosts'));
    }
}
