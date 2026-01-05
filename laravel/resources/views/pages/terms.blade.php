@extends('layouts.public')

@section('title', 'Terms of Service')
@section('description', 'AgentWall Terms of Service.')

@section('content')
<section class="pt-12 pb-8 px-4 bg-white">
    <div class="max-w-4xl mx-auto text-center">
        <span class="text-wall-blue font-semibold text-sm uppercase tracking-wider">Legal</span>
        <h1 class="text-4xl font-extrabold mt-2 mb-4 text-darkest">Terms of Service</h1>
        <p class="text-gray-500">Last updated: January 5, 2026</p>
    </div>
</section>

<section class="py-12 px-4 bg-lighter">
    <div class="max-w-4xl mx-auto">
        <div class="bg-white rounded-2xl border border-gray-200 overflow-hidden">
            <div class="p-8 border-b border-gray-200 bg-gray-50">
                <h2 class="font-bold text-darkest mb-4">Contents</h2>
                <nav class="grid md:grid-cols-2 gap-2 text-sm">
                    <a href="#t1" class="text-wall-blue hover:underline">1. Acceptance of Terms</a>
                    <a href="#t2" class="text-wall-blue hover:underline">2. Description of Service</a>
                    <a href="#t3" class="text-wall-blue hover:underline">3. Account Responsibilities</a>
                    <a href="#t4" class="text-wall-blue hover:underline">4. Acceptable Use</a>
                    <a href="#t5" class="text-wall-blue hover:underline">5. Payment Terms</a>
                    <a href="#t6" class="text-wall-blue hover:underline">6. Limitation of Liability</a>
                </nav>
            </div>
            
            <div class="p-8 space-y-10">
                <section id="t1">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">1</span>
                        Acceptance of Terms
                    </h2>
                    <p class="text-gray-600 leading-relaxed">By accessing or using AgentWall, you agree to be bound by these Terms of Service. If you do not agree, do not use the Service.</p>
                </section>
                
                <section id="t2">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">2</span>
                        Description of Service
                    </h2>
                    <p class="text-gray-600 leading-relaxed mb-4">AgentWall provides an AI agent governance platform including:</p>
                    <div class="grid md:grid-cols-2 gap-3">
                        <div class="bg-lighter rounded-xl p-4 flex items-center gap-3">
                            <svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                            <span class="text-gray-600 text-sm">API proxying to LLM providers</span>
                        </div>
                        <div class="bg-lighter rounded-xl p-4 flex items-center gap-3">
                            <svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                            <span class="text-gray-600 text-sm">Run-level cost tracking</span>
                        </div>
                        <div class="bg-lighter rounded-xl p-4 flex items-center gap-3">
                            <svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                            <span class="text-gray-600 text-sm">Loop detection & kill switch</span>
                        </div>
                        <div class="bg-lighter rounded-xl p-4 flex items-center gap-3">
                            <svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                            <span class="text-gray-600 text-sm">Security & DLP features</span>
                        </div>
                    </div>
                </section>
                
                <section id="t3">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">3</span>
                        Account Responsibilities
                    </h2>
                    <ul class="space-y-2 text-gray-600">
                        <li class="flex items-center gap-2"><svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>Maintain security of your API keys</li>
                        <li class="flex items-center gap-2"><svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>Provide accurate account information</li>
                        <li class="flex items-center gap-2"><svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>Responsible for all activity under your account</li>
                        <li class="flex items-center gap-2"><svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>Notify us of unauthorized access immediately</li>
                    </ul>
                </section>
                
                <section id="t4">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">4</span>
                        Acceptable Use
                    </h2>
                    <p class="text-gray-600 mb-4">You agree NOT to:</p>
                    <div class="bg-alert-red/5 border border-alert-red/20 rounded-xl p-4">
                        <ul class="space-y-2 text-gray-600 text-sm">
                            <li class="flex items-center gap-2"><svg class="w-5 h-5 text-alert-red" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>Use for illegal purposes</li>
                            <li class="flex items-center gap-2"><svg class="w-5 h-5 text-alert-red" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>Bypass security measures or rate limits</li>
                            <li class="flex items-center gap-2"><svg class="w-5 h-5 text-alert-red" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>Interfere with or disrupt the Service</li>
                            <li class="flex items-center gap-2"><svg class="w-5 h-5 text-alert-red" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>Resell without authorization</li>
                        </ul>
                    </div>
                </section>
                
                <section id="t5">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">5</span>
                        Payment Terms
                    </h2>
                    <div class="grid md:grid-cols-2 gap-4">
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Billing</h3>
                            <p class="text-gray-600 text-sm">Monthly or annual billing cycles</p>
                        </div>
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Refunds</h3>
                            <p class="text-gray-600 text-sm">Non-refundable unless stated otherwise</p>
                        </div>
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Price Changes</h3>
                            <p class="text-gray-600 text-sm">30 days notice for any changes</p>
                        </div>
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Overages</h3>
                            <p class="text-gray-600 text-sm">Billed at plan-specified rates</p>
                        </div>
                    </div>
                </section>
                
                <section id="t6">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">6</span>
                        Limitation of Liability
                    </h2>
                    <div class="bg-warning-orange/10 border border-warning-orange/30 rounded-xl p-4">
                        <p class="text-gray-600 text-sm">AgentWall shall not be liable for indirect, incidental, special, or consequential damages. Our total liability shall not exceed the amount paid by you in the 12 months preceding the claim. We strive for 99.9% uptime but do not guarantee uninterrupted access.</p>
                    </div>
                </section>
                
                <section class="pt-6 border-t border-gray-200">
                    <p class="text-gray-600">Questions? Contact <a href="mailto:legal@agentwall.io" class="text-wall-blue hover:underline font-medium">legal@agentwall.io</a></p>
                </section>
            </div>
        </div>
    </div>
</section>
@endsection