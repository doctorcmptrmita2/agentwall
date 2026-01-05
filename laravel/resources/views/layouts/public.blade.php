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
    <nav class="fixed top-0 w-full z-50 bg-white/90 backdrop-blur-lg border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <a href="/" class="flex items-center">
                    <img src="/branding/logo.svg" alt="AgentWall" class="h-10 w-auto">
                </a>
                <div class="hidden md:flex items-center space-x-8">
                    <a href="/#features" class="text-gray-600 hover:text-wall-blue font-medium transition">Features</a>
                    <a href="/#how-it-works" class="text-gray-600 hover:text-wall-blue font-medium transition">How It Works</a>
                    <a href="/#pricing" class="text-gray-600 hover:text-wall-blue font-medium transition">Pricing</a>
                    <a href="/admin" class="gradient-bg hover:opacity-90 text-white px-5 py-2.5 rounded-lg font-semibold transition">Dashboard</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Content -->
    <main class="pt-16">
        @yield('content')
    </main>

    <!-- Footer -->
    <footer class="py-12 px-4 bg-darkest text-white">
        <div class="max-w-7xl mx-auto">
            <div class="grid md:grid-cols-4 gap-8 mb-12">
                <div class="md:col-span-2">
                    <a href="/" class="flex items-center mb-4">
                        <img src="/branding/logo-dark.svg" alt="AgentWall" class="h-10 w-auto">
                    </a>
                    <p class="text-gray-400 mb-4 max-w-sm">The first Agent Firewall for AI. Guard the Agent, Save the Budget.</p>
                    <div class="flex items-center gap-4">
                        <a href="https://twitter.com/agentwall" class="text-gray-400 hover:text-white transition">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                        </a>
                        <a href="https://github.com/agentwall" class="text-gray-400 hover:text-white transition">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"/></svg>
                        </a>
                    </div>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Product</h4>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="/#features" class="hover:text-white transition">Features</a></li>
                        <li><a href="/#pricing" class="hover:text-white transition">Pricing</a></li>
                        <li><a href="https://docs.agentwall.io" class="hover:text-white transition">Documentation</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Company</h4>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="/about" class="hover:text-white transition">About</a></li>
                        <li><a href="/blog" class="hover:text-white transition">Blog</a></li>
                        <li><a href="/contact" class="hover:text-white transition">Contact</a></li>
                        <li><a href="/privacy" class="hover:text-white transition">Privacy</a></li>
                        <li><a href="/terms" class="hover:text-white transition">Terms</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
                <div class="text-gray-500 text-sm mb-4 md:mb-0">© 2026 AgentWall. All rights reserved.</div>
                <div class="text-gray-500 text-sm">Guard the Agent, Save the Budget 🛡️</div>
            </div>
        </div>
    </footer>
</body>
</html>