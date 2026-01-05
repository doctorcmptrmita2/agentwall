@extends('layouts.public')

@section('title', 'Contact')
@section('description', 'Get in touch with the AgentWall team.')

@section('content')
<section class="pt-12 pb-8 px-4 bg-white">
    <div class="max-w-4xl mx-auto text-center">
        <span class="text-wall-blue font-semibold text-sm uppercase tracking-wider">Contact</span>
        <h1 class="text-4xl font-extrabold mt-2 mb-4 text-darkest">Get in Touch</h1>
        <p class="text-xl text-gray-600">Have questions? We're here to help.</p>
    </div>
</section>

<section class="py-12 px-4 bg-lighter">
    <div class="max-w-5xl mx-auto">
        <div class="grid lg:grid-cols-2 gap-8">
            <!-- Contact Options -->
            <div class="space-y-6">
                <div class="bg-white rounded-2xl border border-gray-200 p-6">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                            </svg>
                        </div>
                        <div>
                            <h3 class="font-bold text-darkest mb-1">General Inquiries</h3>
                            <p class="text-gray-600 text-sm mb-2">Questions about AgentWall? We'd love to hear from you.</p>
                            <a href="mailto:hello@agentwall.io" class="text-wall-blue font-semibold hover:underline">hello@agentwall.io</a>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-2xl border border-gray-200 p-6">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 bg-alert-red rounded-xl flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z"/>
                            </svg>
                        </div>
                        <div>
                            <h3 class="font-bold text-darkest mb-1">Technical Support</h3>
                            <p class="text-gray-600 text-sm mb-2">Having issues? Our team is ready to help.</p>
                            <a href="mailto:support@agentwall.io" class="text-wall-blue font-semibold hover:underline">support@agentwall.io</a>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-2xl border border-gray-200 p-6">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 bg-success-green rounded-xl flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                            </svg>
                        </div>
                        <div>
                            <h3 class="font-bold text-darkest mb-1">Enterprise Sales</h3>
                            <p class="text-gray-600 text-sm mb-2">Need custom solutions or self-hosting options?</p>
                            <a href="mailto:sales@agentwall.io" class="text-wall-blue font-semibold hover:underline">sales@agentwall.io</a>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-2xl border border-gray-200 p-6">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center flex-shrink-0">
                            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                            </svg>
                        </div>
                        <div>
                            <h3 class="font-bold text-darkest mb-1">Security Issues</h3>
                            <p class="text-gray-600 text-sm mb-2">Found a vulnerability? Report it responsibly.</p>
                            <a href="mailto:security@agentwall.io" class="text-wall-blue font-semibold hover:underline">security@agentwall.io</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Contact Form -->
            <div class="bg-white rounded-2xl border border-gray-200 p-8">
                <h2 class="text-xl font-bold text-darkest mb-6">Send us a message</h2>
                <form class="space-y-5" x-data="{ submitted: false, loading: false }" @submit.prevent="loading = true; setTimeout(() => { submitted = true; loading = false; }, 1000)">
                    <div x-show="!submitted">
                        <div class="grid md:grid-cols-2 gap-4 mb-4">
                            <div>
                                <label class="block text-sm font-medium text-darkest mb-2">Name</label>
                                <input type="text" required class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-wall-blue focus:outline-none" placeholder="Your name">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-darkest mb-2">Email</label>
                                <input type="email" required class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-wall-blue focus:outline-none" placeholder="you@company.com">
                            </div>
                        </div>
                        
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-darkest mb-2">Subject</label>
                            <select class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-wall-blue focus:outline-none bg-white">
                                <option>General Question</option>
                                <option>Technical Support</option>
                                <option>Enterprise Inquiry</option>
                                <option>Partnership</option>
                                <option>Other</option>
                            </select>
                        </div>
                        
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-darkest mb-2">Message</label>
                            <textarea required rows="5" class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-wall-blue focus:outline-none resize-none" placeholder="How can we help?"></textarea>
                        </div>
                        
                        <button type="submit" class="w-full gradient-bg hover:opacity-90 text-white px-6 py-4 rounded-xl font-semibold transition flex items-center justify-center gap-2" :disabled="loading">
                            <span x-show="!loading">Send Message</span>
                            <span x-show="loading" class="flex items-center gap-2">
                                <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                                </svg>
                                Sending...
                            </span>
                        </button>
                    </div>
                    
                    <div x-show="submitted" x-transition class="text-center py-8">
                        <div class="w-16 h-16 bg-success-green/10 rounded-full flex items-center justify-center mx-auto mb-4">
                            <svg class="w-8 h-8 text-success-green" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                        </div>
                        <h3 class="text-xl font-bold text-darkest mb-2">Message Sent!</h3>
                        <p class="text-gray-600">We'll get back to you within 24 hours.</p>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Social Links -->
        <div class="mt-12 text-center">
            <h3 class="font-bold text-darkest mb-4">Connect with us</h3>
            <div class="flex items-center justify-center gap-4">
                <a href="https://twitter.com/agentwall" class="w-12 h-12 bg-white border border-gray-200 rounded-xl flex items-center justify-center text-gray-600 hover:text-wall-blue hover:border-wall-blue transition">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                </a>
                <a href="https://github.com/agentwall" class="w-12 h-12 bg-white border border-gray-200 rounded-xl flex items-center justify-center text-gray-600 hover:text-wall-blue hover:border-wall-blue transition">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"/></svg>
                </a>
                <a href="https://discord.gg/agentwall" class="w-12 h-12 bg-white border border-gray-200 rounded-xl flex items-center justify-center text-gray-600 hover:text-wall-blue hover:border-wall-blue transition">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189z"/></svg>
                </a>
                <a href="https://linkedin.com/company/agentwall" class="w-12 h-12 bg-white border border-gray-200 rounded-xl flex items-center justify-center text-gray-600 hover:text-wall-blue hover:border-wall-blue transition">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                </a>
            </div>
        </div>
    </div>
</section>
@endsection