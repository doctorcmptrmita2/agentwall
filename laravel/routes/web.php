<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/about', function () {
    return view('pages.about');
});

Route::get('/privacy', function () {
    return view('pages.privacy');
});

Route::get('/terms', function () {
    return view('pages.terms');
});

Route::get('/contact', function () {
    return view('pages.contact');
});

Route::get('/blog', [\App\Http\Controllers\BlogController::class, 'index']);
Route::get('/blog/{slug}', [\App\Http\Controllers\BlogController::class, 'show']);
