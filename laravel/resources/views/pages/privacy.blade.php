@extends('layouts.public')

@section('title', 'Privacy Policy')
@section('description', 'AgentWall Privacy Policy - How we handle your data.')

@section('content')
<section class="pt-12 pb-8 px-4 bg-white">
    <div class="max-w-4xl mx-auto text-center">
        <span class="text-wall-blue font-semibold text-sm uppercase tracking-wider">Legal</span>
        <h1 class="text-4xl font-extrabold mt-2 mb-4 text-darkest">Privacy Policy</h1>
        <p class="text-gray-500">Last updated: January 5, 2026</p>
    </div>
</section>

<section class="py-12 px-4 bg-lighter">
    <div class="max-w-4xl mx-auto">
        <div class="bg-white rounded-2xl border border-gray-200 overflow-hidden">
            <div class="p-8 border-b border-gray-200 bg-gray-50">
                <h2 class="font-bold text-darkest mb-4">Contents</h2>
                <nav class="grid md:grid-cols-2 gap-2 text-sm">
                    <a href="#p1" class="text-wall-blue hover:underline">1. Introduction</a>
                    <a href="#p2" class="text-wall-blue hover:underline">2. Information We Collect</a>
                    <a href="#p3" class="text-wall-blue hover:underline">3. How We Use Information</a>
                    <a href="#p4" class="text-wall-blue hover:underline">4. Data Security</a>
                    <a href="#p5" class="text-wall-blue hover:underline">5. Data Retention</a>
                    <a href="#p6" class="text-wall-blue hover:underline">6. Your Rights</a>
                </nav>
            </div>
            
            <div class="p-8 space-y-10">
                <section id="p1">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">1</span>
                        Introduction
                    </h2>
                    <p class="text-gray-600 leading-relaxed">AgentWall is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our AI agent governance platform.</p>
                </section>
                
                <section id="p2">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">2</span>
                        Information We Collect
                    </h2>
                    <p class="text-gray-600 leading-relaxed mb-4">We collect information in the following ways:</p>
                    <div class="grid md:grid-cols-2 gap-3">
                        <div class="bg-lighter rounded-xl p-4 flex items-center gap-3">
                            <svg class="w-5 h-5 text-wall-blue flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                            <span class="text-gray-600 text-sm">Account info (email, name, company)</span>
                        </div>
                        <div class="bg-lighter rounded-xl p-4 flex items-center gap-3">
                            <svg class="w-5 h-5 text-wall-blue flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                            <span class="text-gray-600 text-sm">Usage data (tokens, costs, metrics)</span>
                        </div>
                        <div class="bg-lighter rounded-xl p-4 flex items-center gap-3">
                            <svg class="w-5 h-5 text-wall-blue flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                            <span class="text-gray-600 text-sm">Log data (only if enabled by you)</span>
                        </div>
                        <div class="bg-lighter rounded-xl p-4 flex items-center gap-3">
                            <svg class="w-5 h-5 text-wall-blue flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                            <span class="text-gray-600 text-sm">Billing information</span>
                        </div>
                    </div>
                </section>
                
                <section id="p3">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">3</span>
                        How We Use Information
                    </h2>
                    <ul class="space-y-2 text-gray-600">
                        <li class="flex items-center gap-2"><svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>Provide and improve our service</li>
                        <li class="flex items-center gap-2"><svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>Detect loops and anomalies</li>
                        <li class="flex items-center gap-2"><svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>Calculate cost metrics and analytics</li>
                        <li class="flex items-center gap-2"><svg class="w-5 h-5 text-wall-blue" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>Send budget and security alerts</li>
                    </ul>
                </section>
                
                <section id="p4">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">4</span>
                        Data Security
                    </h2>
                    <div class="bg-wall-blue/5 border border-wall-blue/20 rounded-xl p-4">
                        <ul class="space-y-2 text-gray-600 text-sm">
                            <li class="flex items-center gap-2"><svg class="w-5 h-5 text-success-green" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>TLS 1.3 encryption in transit</li>
                            <li class="flex items-center gap-2"><svg class="w-5 h-5 text-success-green" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>AES-256 encryption at rest</li>
                            <li class="flex items-center gap-2"><svg class="w-5 h-5 text-success-green" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>API keys hashed (never plain text)</li>
                            <li class="flex items-center gap-2"><svg class="w-5 h-5 text-success-green" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>Regular security audits</li>
                        </ul>
                    </div>
                </section>
                
                <section id="p5">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">5</span>
                        Data Retention
                    </h2>
                    <div class="grid md:grid-cols-2 gap-4 mb-4">
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Log Data</h3>
                            <p class="text-gray-600 text-sm">90 days (configurable)</p>
                        </div>
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Metrics</h3>
                            <p class="text-gray-600 text-sm">1 year aggregated</p>
                        </div>
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Account Info</h3>
                            <p class="text-gray-600 text-sm">Until account deletion</p>
                        </div>
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Zero Retention</h3>
                            <p class="text-gray-600 text-sm">Enterprise option available</p>
                        </div>
                    </div>
                    <div class="bg-success-green/10 border border-success-green/30 rounded-xl p-4">
                        <p class="text-gray-600 text-sm"><strong class="text-darkest">Zero Retention Mode:</strong> Enterprise customers can enable Zero Retention Mode where no prompt or response content is ever stored.</p>
                    </div>
                </section>
                
                <section id="p6">
                    <h2 class="text-xl font-bold text-darkest mb-4 flex items-center gap-3">
                        <span class="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center text-white text-sm font-bold">6</span>
                        Your Rights
                    </h2>
                    <div class="grid md:grid-cols-2 gap-4">
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Access</h3>
                            <p class="text-gray-600 text-sm">Request a copy of your personal data</p>
                        </div>
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Deletion</h3>
                            <p class="text-gray-600 text-sm">Request deletion of your data</p>
                        </div>
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Export</h3>
                            <p class="text-gray-600 text-sm">Download your data in portable format</p>
                        </div>
                        <div class="bg-lighter rounded-xl p-4">
                            <h3 class="font-semibold text-darkest mb-1">Opt-out</h3>
                            <p class="text-gray-600 text-sm">Unsubscribe from marketing emails</p>
                        </div>
                    </div>
                </section>
                
                <section class="pt-6 border-t border-gray-200">
                    <p class="text-gray-600">Questions? Contact <a href="mailto:privacy@agentwall.io" class="text-wall-blue hover:underline font-medium">privacy@agentwall.io</a></p>
                </section>
            </div>
        </div>
    </div>
</section>
@endsection
