<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'AgentWall') - Guard the Agent, Save the Budget</title>
    <meta name="description" content="@yield('description', 'The first Agent Firewall for AI. Stop runaway agents, prevent infinite loops, and control your AI costs in real-time.')">
    
    <link rel="icon" type="image/svg+xml" href="/branding/logo-icon.svg">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'wall-blue': '#2563EB',
                        'wall-blue-dark': '#1D4ED8',
                        'wall-blue-light': '#3B82F6',
                        'alert-red': '#DC2626',
                        'success-green': '#16A34A',
                        'warning-orange': '#F59E0B',
                        'dark': '#1F2937',
                        'darker': '#111827',
                        'darkest': '#0F172A',
                        'light': '#F3F4F6',
                        'lighter': '#F9FAFB',
                    },
                    fontFamily: {
                        'sans': ['Inter', 'system-ui', 'sans-serif'],
                        'mono': ['JetBrains Mono', 'monospace'],
                    }
                }
            }
        }
    </script>
    
    <style>
        .gradient-bg { background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); }
    </style>
    @yield('head')
</head>
<body class="bg-lighter text-dark antialiased font-sans">
    <!-- Navigation -->
    <nav class="fixed top-0 w-full z-50 bg-white/90 backdrop-blur-lg border-b border-gray-200" x-data="{ mobileMenuOpen: false }">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Logo -->
                <a href="/" class="flex items-center z-50">
                    <img src="/branding/logo.svg" alt="AgentWall" class="h-8 sm:h-10 w-auto">
                </a>
                
                <!-- Desktop Menu -->
                <div class="hidden md:flex items-center space-x-8">
                    <a href="/#features" class="text-gray-600 hover:text-wall-blue font-medium transition">Features</a>
                    <a href="/#how-it-works" class="text-gray-600 hover:text-wall-blue font-medium transition">How It Works</a>
                    <a href="/#pricing" class="text-gray-600 hover:text-wall-blue font-medium transition">Pricing</a>
                    <a href="/blog" class="text-gray-600 hover:text-wall-blue font-medium transition">Blog</a>
                    <a href="/admin" class="gradient-bg hover:opacity-90 text-white px-5 py-2.5 rounded-lg font-semibold transition">Dashboard</a>
                </div>

                <!-- Mobile Menu Button -->
                <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden z-50 p-2 rounded-lg hover:bg-gray-100 transition" aria-label="Toggle menu">
                    <svg x-show="!mobileMenuOpen" class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                    </svg>
                    <svg x-show="mobileMenuOpen" class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" x-cloak>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>
        </div>

        <!-- Mobile Off-Canvas Menu -->
        <div x-show="mobileMenuOpen" 
             x-transition:enter="transition ease-out duration-300"
             x-transition:enter-start="opacity-0"
             x-transition:enter-end="opacity-100"
             x-transition:leave="transition ease-in duration-200"
             x-transition:leave-start="opacity-100"
             x-transition:leave-end="opacity-0"
             @click="mobileMenuOpen = false"
             class="fixed inset-0 bg-black/50 backdrop-blur-sm md:hidden z-40"
             x-cloak>
        </div>

        <div x-show="mobileMenuOpen"
             x-transition:enter="transition ease-out duration-300 transform"
             x-transition:enter-start="-translate-x-full"
             x-transition:enter-end="translate-x-0"
             x-transition:leave="transition ease-in duration-200 transform"
             x-transition:leave-start="translate-x-0"
             x-transition:leave-end="-translate-x-full"
             class="fixed top-0 left-0 h-full w-80 bg-white shadow-2xl md:hidden z-40 overflow-y-auto"
             x-cloak>
            
            <!-- Mobile Menu Header -->
            <div class="p-6 border-b border-gray-200">
                <div class="flex items-center gap-3">
                    <div class="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-blue-700 shadow-lg">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                        </svg>
                    </div>
                    <div>
                        <h2 class="text-xl font-bold">
                            <span class="text-gray-900">Agent</span><span class="text-blue-600">Wall</span>
                        </h2>
                        <p class="text-xs text-gray-500">Guard the Agent</p>
                    </div>
                </div>
            </div>

            <!-- Mobile Menu Links -->
            <div class="p-6 space-y-1">
                <a href="/" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-50 transition group">
                    <svg class="w-5 h-5 text-gray-400 group-hover:text-wall-blue transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                    </svg>
                    <span class="font-medium text-gray-700 group-hover:text-wall-blue transition">Home</span>
                </a>
                
                <a href="/#features" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-50 transition group">
                    <svg class="w-5 h-5 text-gray-400 group-hover:text-wall-blue transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                    </svg>
                    <span class="font-medium text-gray-700 group-hover:text-wall-blue transition">Features</span>
                </a>
                
                <a href="/#how-it-works" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-50 transition group">
                    <svg class="w-5 h-5 text-gray-400 group-hover:text-wall-blue transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                    </svg>
                    <span class="font-medium text-gray-700 group-hover:text-wall-blue transition">How It Works</span>
                </a>
                
                <a href="/#pricing" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-50 transition group">
                    <svg class="w-5 h-5 text-gray-400 group-hover:text-wall-blue transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <span class="font-medium text-gray-700 group-hover:text-wall-blue transition">Pricing</span>
                </a>
                
                <a href="/blog" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-50 transition group">
                    <svg class="w-5 h-5 text-gray-400 group-hover:text-wall-blue transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
                    </svg>
                    <span class="font-medium text-gray-700 group-hover:text-wall-blue transition">Blog</span>
                </a>

                <div class="pt-4 mt-4 border-t border-gray-200">
                    <a href="/about" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-50 transition group">
                        <svg class="w-5 h-5 text-gray-400 group-hover:text-wall-blue transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        <span class="font-medium text-gray-700 group-hover:text-wall-blue transition">About</span>
                    </a>
                    
                    <a href="/contact" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-50 transition group">
                        <svg class="w-5 h-5 text-gray-400 group-hover:text-wall-blue transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                        </svg>
                        <span class="font-medium text-gray-700 group-hover:text-wall-blue transition">Contact</span>
                    </a>
                </div>

                <div class="pt-4">
                    <a href="/admin" class="flex items-center justify-center gap-2 w-full gradient-bg hover:opacity-90 text-white px-6 py-3 rounded-lg font-semibold transition shadow-lg">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                        </svg>
                        <span>Dashboard</span>
                    </a>
                </div>
            </div>

            <!-- Mobile Menu Footer -->
            <div class="absolute bottom-0 left-0 right-0 p-6 border-t border-gray-200 bg-gray-50">
                <p class="text-xs text-gray-500 text-center mb-3">Guard the Agent, Save the Budget</p>
                <div class="flex items-center justify-center gap-4">
                    <a href="https://twitter.com/agentwall" class="text-gray-400 hover:text-wall-blue transition">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    </a>
                    <a href="https://github.com/agentwall" class="text-gray-400 hover:text-wall-blue transition">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"/></svg>
                    </a>
                </div>
            </div>
        </div>
    </nav>

    <style>
        [x-cloak] { display: none !important; }
    </style>

    <!-- Content -->
    <main class="pt-16">
        @yield('content')
    </main>

    <!-- Footer -->
    <footer class="py-12 px-4 bg-darkest text-white">
        <div class="max-w-7xl mx-auto">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
                <div class="sm:col-span-2 lg:col-span-2">
                    <a href="/" class="flex items-center mb-4">
                        <img src="/branding/logo-dark.svg" alt="AgentWall" class="h-10 w-auto">
                    </a>
                    <p class="text-gray-400 mb-4 max-w-sm text-sm sm:text-base">The first Agent Firewall for AI. Guard the Agent, Save the Budget.</p>
                    <div class="flex items-center gap-4">
                        <a href="https://twitter.com/agentwall" class="text-gray-400 hover:text-white transition" aria-label="Twitter">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                        </a>
                        <a href="https://github.com/agentwall" class="text-gray-400 hover:text-white transition" aria-label="GitHub">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"/></svg>
                        </a>
                    </div>
                </div>
                <div>
                    <h4 class="font-semibold mb-4 text-base sm:text-lg">Product</h4>
                    <ul class="space-y-2 text-gray-400 text-sm sm:text-base">
                        <li><a href="/#features" class="hover:text-white transition">Features</a></li>
                        <li><a href="/#pricing" class="hover:text-white transition">Pricing</a></li>
                        <li><a href="https://docs.agentwall.io" class="hover:text-white transition">Documentation</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-4 text-base sm:text-lg">Company</h4>
                    <ul class="space-y-2 text-gray-400 text-sm sm:text-base">
                        <li><a href="/about" class="hover:text-white transition">About</a></li>
                        <li><a href="/blog" class="hover:text-white transition">Blog</a></li>
                        <li><a href="/contact" class="hover:text-white transition">Contact</a></li>
                        <li><a href="/privacy" class="hover:text-white transition">Privacy</a></li>
                        <li><a href="/terms" class="hover:text-white transition">Terms</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 pt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
                <div class="text-gray-500 text-xs sm:text-sm text-center sm:text-left">© 2026 AgentWall. All rights reserved.</div>
                <div class="text-gray-500 text-xs sm:text-sm">Guard the Agent, Save the Budget 🛡️</div>
            </div>
        </div>
    </footer>
</body>
</html>