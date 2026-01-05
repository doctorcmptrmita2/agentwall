@extends('layouts.public')

@section('title', 'About')
@section('description', 'Learn about AgentWall - The first Agent Firewall for AI.')

@section('content')
<!-- Hero -->
<section class="pt-16 pb-12 px-4 bg-white">
    <div class="max-w-4xl mx-auto text-center">
        <span class="text-wall-blue font-semibold text-sm uppercase tracking-wider">About Us</span>
        <h1 class="text-4xl md:text-5xl font-extrabold mt-3 mb-6 text-darkest">
            Guard the Agent,<br>
            <span class="text-wall-blue">Save the Budget</span>
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
            We're building the control layer that AI agents need. Because autonomous doesn't mean uncontrolled.
        </p>
    </div>
</section>

<!-- Problem/Solution -->
<section class="py-16 px-4 bg-lighter">
    <div class="max-w-5xl mx-auto">
        <div class="grid md:grid-cols-2 gap-8">
            <!-- Problem -->
            <div class="bg-white rounded-2xl border border-gray-200 p-8">
                <div class="w-12 h-12 bg-alert-red/10 rounded-xl flex items-center justify-center mb-6">
                    <svg class="w-6 h-6 text-alert-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                </div>
                <h2 class="text-2xl font-bold text-darkest mb-4">The Problem</h2>
                <p class="text-gray-600 leading-relaxed mb-4">
                    AI agents are powerful but unpredictable. A single bug can trigger infinite loops, burning through thousands of dollars in API costs overnight.
                </p>
                <ul class="space-y-2 text-gray-600 text-sm">
                    <li class="flex items-center gap-2">
                        <svg class="w-4 h-4 text-alert-red" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
                        Runaway agents with no kill switch
                    </li>
                    <li class="flex items-center gap-2">
                        <svg class="w-4 h-4 text-alert-red" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
                        Unexpected $50K bills from infinite loops
                    </li>
                    <li class="flex items-center gap-2">
                        <svg class="w-4 h-4 text-alert-red" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>
                        Zero visibility into agent behavior
                    </li>
                </ul>
            </div>
            
            <!-- Solution -->
            <div class="bg-white rounded-2xl border border-gray-200 p-8">
                <div class="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center mb-6">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                    </svg>
                </div>
                <h2 class="text-2xl font-bold text-darkest mb-4">Our Solution</h2>
                <p class="text-gray-600 leading-relaxed mb-4">
                    AgentWall is the firewall between your agents and chaos. We track every run, detect anomalies, and give you instant control.
                </p>
                <ul class="space-y-2 text-gray-600 text-sm">
                    <li class="flex items-center gap-2">
                        <svg class="w-4 h-4 text-success-green" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                        Run-level tracking & budgets
                    </li>
                    <li class="flex items-center gap-2">
                        <svg class="w-4 h-4 text-success-green" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                        Automatic loop detection & kill switch
                    </li>
                    <li class="flex items-center gap-2">
                        <svg class="w-4 h-4 text-success-green" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                        Real-time alerts & governance
                    </li>
                </ul>
            </div>
        </div>
    </div>
</section>

<!-- Core Values -->
<section class="py-16 px-4 bg-white">
    <div class="max-w-5xl mx-auto">
        <div class="text-center mb-12">
            <h2 class="text-3xl font-bold text-darkest">What We Believe</h2>
        </div>
        
        <div class="grid md:grid-cols-3 gap-6">
            <div class="text-center p-6">
                <div class="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-darkest mb-2">Speed Matters</h3>
                <p class="text-gray-600 text-sm">Less than 10ms overhead. We never slow down your agents.</p>
            </div>
            
            <div class="text-center p-6">
                <div class="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-darkest mb-2">Full Visibility</h3>
                <p class="text-gray-600 text-sm">See every step, every token, every dollar. No black boxes.</p>
            </div>
            
            <div class="text-center p-6">
                <div class="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-darkest mb-2">Privacy First</h3>
                <p class="text-gray-600 text-sm">Self-host option. Zero retention mode. Your data stays yours.</p>
            </div>
        </div>
    </div>
</section>

<!-- Stats -->
<section class="py-16 px-4 bg-darkest">
    <div class="max-w-5xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
                <div class="text-4xl font-extrabold text-white mb-1">&lt;10ms</div>
                <div class="text-gray-400 text-sm">Proxy Overhead</div>
            </div>
            <div>
                <div class="text-4xl font-extrabold text-white mb-1">99.9%</div>
                <div class="text-gray-400 text-sm">Uptime SLA</div>
            </div>
            <div>
                <div class="text-4xl font-extrabold text-white mb-1">100%</div>
                <div class="text-gray-400 text-sm">OpenAI Compatible</div>
            </div>
            <div>
                <div class="text-4xl font-extrabold text-white mb-1">$0</div>
                <div class="text-gray-400 text-sm">Surprise Bills</div>
            </div>
        </div>
    </div>
</section>

<!-- CTA -->
<section class="py-16 px-4 bg-lighter">
    <div class="max-w-3xl mx-auto text-center">
        <h2 class="text-3xl font-bold text-darkest mb-4">Ready to take control?</h2>
        <p class="text-gray-600 mb-8">Start protecting your AI agents today. No credit card required.</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/register" class="gradient-bg hover:opacity-90 text-white px-8 py-4 rounded-xl font-semibold transition inline-flex items-center justify-center gap-2">
                Get Started Free
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                </svg>
            </a>
            <a href="/contact" class="bg-white border-2 border-gray-200 hover:border-wall-blue text-darkest px-8 py-4 rounded-xl font-semibold transition inline-flex items-center justify-center gap-2">
                Talk to Sales
            </a>
        </div>
    </div>
</section>
@endsection
