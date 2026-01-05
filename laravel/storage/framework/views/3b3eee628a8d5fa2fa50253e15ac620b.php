<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgentWall - Guard the Agent, Save the Budget</title>
    <meta name="description" content="The first Agent Firewall for AI. Stop runaway agents, prevent infinite loops, and control your AI costs in real-time.">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="/branding/logoA.png">
    
    <!-- Google Fonts - Inter & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
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
    
    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    
    <style>
        .gradient-text {
            background: linear-gradient(135deg, #2563EB 0%, #3B82F6 50%, #60A5FA 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .gradient-bg {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        }
        .glow-blue {
            box-shadow: 0 0 40px rgba(37, 99, 235, 0.3);
        }
        .card-hover {
            transition: all 0.3s ease;
        }
        .card-hover:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
        .code-block {
            background: linear-gradient(135deg, #1F2937 0%, #111827 100%);
        }
        .hero-pattern {
            background-image: 
                radial-gradient(circle at 25% 25%, rgba(37, 99, 235, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, rgba(37, 99, 235, 0.05) 0%, transparent 50%);
        }
    </style>
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
                    <a href="#features" class="text-gray-600 hover:text-wall-blue font-medium transition">Features</a>
                    <a href="#how-it-works" class="text-gray-600 hover:text-wall-blue font-medium transition">How It Works</a>
                    <a href="#pricing" class="text-gray-600 hover:text-wall-blue font-medium transition">Pricing</a>
                    <a href="https://docs.agentwall.io" class="text-gray-600 hover:text-wall-blue font-medium transition">Docs</a>
                    <a href="/admin" class="gradient-bg hover:opacity-90 text-white px-5 py-2.5 rounded-lg font-semibold transition">Dashboard</a>
                </div>
                <!-- Mobile menu button -->
                <button class="md:hidden p-2" x-data x-on:click="$dispatch('toggle-mobile-menu')">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                    </svg>
                </button>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-28 pb-20 px-4 hero-pattern bg-white">
        <div class="max-w-7xl mx-auto">
            <div class="grid lg:grid-cols-2 gap-12 items-center">
                <!-- Left: Content -->
                <div>
                    <div class="inline-flex items-center px-4 py-2 rounded-full bg-wall-blue/10 border border-wall-blue/20 mb-6">
                        <span class="w-2 h-2 bg-success-green rounded-full mr-2 animate-pulse"></span>
                        <span class="text-wall-blue text-sm font-semibold">Now in Public Beta</span>
                    </div>
                    
                    <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold mb-6 leading-tight text-darkest">
                        <span class="gradient-text">Guard the Agent,</span><br>
                        Save the Budget
                    </h1>
                    
                    <p class="text-lg md:text-xl text-gray-600 mb-8 leading-relaxed">
                        The first <span class="text-wall-blue font-semibold">Agent Firewall</span> for AI. 
                        Stop runaway agents, prevent infinite loops, and control your AI costs in real-time.
                    </p>
                    
                    <div class="flex flex-col sm:flex-row gap-4 mb-8">
                        <a href="#waitlist" class="gradient-bg hover:opacity-90 text-white px-8 py-4 rounded-xl font-semibold text-lg transition transform hover:scale-[1.02] glow-blue text-center">
                            Get Early Access
                        </a>
                        <a href="#how-it-works" class="border-2 border-gray-300 hover:border-wall-blue text-dark hover:text-wall-blue px-8 py-4 rounded-xl font-semibold text-lg transition text-center">
                            See How It Works
                        </a>
                    </div>
                    
                    <!-- Trust badges -->
                    <div class="flex items-center gap-6 text-sm text-gray-500">
                        <div class="flex items-center gap-2">
                            <svg class="w-5 h-5 text-success-green" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            <span>OpenAI Compatible</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <svg class="w-5 h-5 text-success-green" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            <span>&lt;10ms Latency</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <svg class="w-5 h-5 text-success-green" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            <span>Self-Host Option</span>
                        </div>
                    </div>
                </div>
                
                <!-- Right: Code Example -->
                <div class="code-block rounded-2xl p-6 border border-gray-700 glow-blue">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center space-x-2">
                            <div class="w-3 h-3 rounded-full bg-alert-red"></div>
                            <div class="w-3 h-3 rounded-full bg-warning-orange"></div>
                            <div class="w-3 h-3 rounded-full bg-success-green"></div>
                        </div>
                        <span class="text-gray-500 text-sm font-mono">Just change your base_url</span>
                    </div>
                    <pre class="text-sm md:text-base overflow-x-auto font-mono"><code class="text-gray-300"><span class="text-purple-400">from</span> openai <span class="text-purple-400">import</span> OpenAI

client = OpenAI(
    <span class="text-wall-blue-light">base_url</span>=<span class="text-success-green">"https://api.agentwall.io/v1"</span>,
    <span class="text-wall-blue-light">api_key</span>=<span class="text-success-green">"your-openai-key"</span>
)

<span class="text-gray-500"># Your agent code stays exactly the same</span>
response = client.chat.completions.create(
    <span class="text-wall-blue-light">model</span>=<span class="text-success-green">"gpt-4o"</span>,
    <span class="text-wall-blue-light">messages</span>=[{<span class="text-success-green">"role"</span>: <span class="text-success-green">"user"</span>, ...}],
    <span class="text-wall-blue-light">extra_headers</span>={
        <span class="text-success-green">"X-Run-ID"</span>: <span class="text-success-green">"task-123"</span>,  <span class="text-gray-500"># Track runs</span>
        <span class="text-success-green">"X-Budget-USD"</span>: <span class="text-success-green">"5.00"</span>    <span class="text-gray-500"># Set limits</span>
    }
)</code></pre>
                </div>
            </div>
        </div>
    </section>

    <!-- Problem Section -->
    <section class="py-20 px-4 bg-darkest text-white">
        <div class="max-w-7xl mx-auto">
            <div class="text-center mb-16">
                <h2 class="text-3xl md:text-4xl font-bold mb-4">The $50,000 Wake-Up Call</h2>
                <p class="text-xl text-gray-400 max-w-2xl mx-auto">AI agents are powerful. Uncontrolled agents are expensive.</p>
            </div>
            
            <div class="grid md:grid-cols-3 gap-8">
                <div class="bg-alert-red/10 border border-alert-red/30 rounded-2xl p-8 card-hover">
                    <div class="w-14 h-14 bg-alert-red/20 rounded-xl flex items-center justify-center mb-5">
                        <svg class="w-7 h-7 text-alert-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 text-alert-red">Runaway Costs</h3>
                    <p class="text-gray-400">"Our agent ran overnight and spent $47,000 on GPT-4 calls. No alerts, no limits."</p>
                </div>
                
                <div class="bg-warning-orange/10 border border-warning-orange/30 rounded-2xl p-8 card-hover">
                    <div class="w-14 h-14 bg-warning-orange/20 rounded-xl flex items-center justify-center mb-5">
                        <svg class="w-7 h-7 text-warning-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 text-warning-orange">Infinite Loops</h3>
                    <p class="text-gray-400">"The agent got stuck asking the same question 10,000 times. We only found out from the bill."</p>
                </div>
                
                <div class="bg-purple-500/10 border border-purple-500/30 rounded-2xl p-8 card-hover">
                    <div class="w-14 h-14 bg-purple-500/20 rounded-xl flex items-center justify-center mb-5">
                        <svg class="w-7 h-7 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 text-purple-400">Data Leaks</h3>
                    <p class="text-gray-400">"An agent accidentally sent customer PII to the LLM. Compliance nightmare."</p>
                </div>
            </div>
        </div>
    </section>
</body>
</html>


    <!-- Features Section -->
    <section id="features" class="py-20 px-4 bg-white">
        <div class="max-w-7xl mx-auto">
            <div class="text-center mb-16">
                <span class="text-wall-blue font-semibold text-sm uppercase tracking-wider">Features</span>
                <h2 class="text-3xl md:text-4xl font-bold mt-2 mb-4 text-darkest">Agent Governance, Not Just Gateway</h2>
                <p class="text-xl text-gray-600 max-w-2xl mx-auto">We track entire agent runs, not just individual requests. That's the difference.</p>
            </div>
            
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div class="bg-lighter border border-gray-200 rounded-2xl p-8 card-hover">
                    <div class="w-14 h-14 gradient-bg rounded-xl flex items-center justify-center mb-5">
                        <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 text-darkest">Run-Level Tracking</h3>
                    <p class="text-gray-600">Track entire agent tasks, not just API calls. See the full picture of what your agent is doing across multiple steps.</p>
                </div>
                
                <div class="bg-lighter border border-gray-200 rounded-2xl p-8 card-hover">
                    <div class="w-14 h-14 bg-alert-red rounded-xl flex items-center justify-center mb-5">
                        <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 text-darkest">Kill Switch</h3>
                    <p class="text-gray-600">Stop any agent run instantly from the dashboard. No more waiting for runaway processes to drain your budget.</p>
                </div>
                
                <div class="bg-lighter border border-gray-200 rounded-2xl p-8 card-hover">
                    <div class="w-14 h-14 bg-warning-orange rounded-xl flex items-center justify-center mb-5">
                        <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 text-darkest">Loop Detection</h3>
                    <p class="text-gray-600">Automatically detect and stop infinite loops before they drain your budget. Smart similarity matching catches subtle patterns.</p>
                </div>
                
                <div class="bg-lighter border border-gray-200 rounded-2xl p-8 card-hover">
                    <div class="w-14 h-14 bg-success-green rounded-xl flex items-center justify-center mb-5">
                        <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 text-darkest">Run-Level Budgets</h3>
                    <p class="text-gray-600">"This task can't spend more than $5" - enforce budgets per run, not just per API key. Real cost control.</p>
                </div>
                
                <div class="bg-lighter border border-gray-200 rounded-2xl p-8 card-hover">
                    <div class="w-14 h-14 gradient-bg rounded-xl flex items-center justify-center mb-5">
                        <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 text-darkest">&lt;10ms Overhead</h3>
                    <p class="text-gray-600">Ultra-low latency proxy. Your agents won't even notice we're there. Performance is non-negotiable.</p>
                </div>
                
                <div class="bg-lighter border border-gray-200 rounded-2xl p-8 card-hover">
                    <div class="w-14 h-14 bg-purple-500 rounded-xl flex items-center justify-center mb-5">
                        <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                        </svg>
                    </div>
                    <h3 class="text-xl font-bold mb-3 text-darkest">DLP & PII Protection</h3>
                    <p class="text-gray-600">Automatically detect and mask sensitive data before it reaches the LLM. Stay compliant, stay safe.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- How It Works -->
    <section id="how-it-works" class="py-20 px-4 bg-lighter">
        <div class="max-w-7xl mx-auto">
            <div class="text-center mb-16">
                <span class="text-wall-blue font-semibold text-sm uppercase tracking-wider">How It Works</span>
                <h2 class="text-3xl md:text-4xl font-bold mt-2 mb-4 text-darkest">Three Steps to Agent Safety</h2>
            </div>
            
            <div class="grid md:grid-cols-3 gap-8">
                <div class="text-center">
                    <div class="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold">1</div>
                    <h3 class="text-xl font-bold mb-3 text-darkest">Change Your Base URL</h3>
                    <p class="text-gray-600">Point your OpenAI client to api.agentwall.io. That's it. No SDK changes, no code rewrites.</p>
                </div>
                
                <div class="text-center">
                    <div class="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold">2</div>
                    <h3 class="text-xl font-bold mb-3 text-darkest">Set Your Limits</h3>
                    <p class="text-gray-600">Configure budgets, step limits, and loop detection thresholds via headers or dashboard.</p>
                </div>
                
                <div class="text-center">
                    <div class="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold">3</div>
                    <h3 class="text-xl font-bold mb-3 text-darkest">Sleep Peacefully</h3>
                    <p class="text-gray-600">AgentWall monitors, alerts, and stops runaway agents automatically. You stay in control.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="py-16 px-4 gradient-bg">
        <div class="max-w-5xl mx-auto">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center text-white">
                <div>
                    <div class="text-4xl md:text-5xl font-bold mb-2">&lt;10ms</div>
                    <div class="text-blue-200">Proxy Overhead</div>
                </div>
                <div>
                    <div class="text-4xl md:text-5xl font-bold mb-2">100%</div>
                    <div class="text-blue-200">OpenAI Compatible</div>
                </div>
                <div>
                    <div class="text-4xl md:text-5xl font-bold mb-2">99.9%</div>
                    <div class="text-blue-200">Uptime SLA</div>
                </div>
                <div>
                    <div class="text-4xl md:text-5xl font-bold mb-2">$0</div>
                    <div class="text-blue-200">To Get Started</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="py-20 px-4 bg-white">
        <div class="max-w-7xl mx-auto">
            <div class="text-center mb-16">
                <span class="text-wall-blue font-semibold text-sm uppercase tracking-wider">Pricing</span>
                <h2 class="text-3xl md:text-4xl font-bold mt-2 mb-4 text-darkest">Simple, Transparent Pricing</h2>
                <p class="text-xl text-gray-600">Start free. Scale as you grow.</p>
            </div>
            
            <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                <!-- Free -->
                <div class="bg-lighter border border-gray-200 rounded-2xl p-8">
                    <h3 class="text-xl font-bold mb-2 text-darkest">Starter</h3>
                    <div class="text-4xl font-bold text-darkest mb-1">$0</div>
                    <div class="text-gray-500 mb-6">Forever free</div>
                    <ul class="space-y-3 mb-8">
                        <li class="flex items-center gap-3 text-gray-600">
                            <svg class="w-5 h-5 text-success-green flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            1,000 requests/month
                        </li>
                        <li class="flex items-center gap-3 text-gray-600">
                            <svg class="w-5 h-5 text-success-green flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            Basic loop detection
                        </li>
                        <li class="flex items-center gap-3 text-gray-600">
                            <svg class="w-5 h-5 text-success-green flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            7-day log retention
                        </li>
                    </ul>
                    <a href="#waitlist" class="block text-center border-2 border-gray-300 hover:border-wall-blue text-dark hover:text-wall-blue px-6 py-3 rounded-xl font-semibold transition">
                        Get Started
                    </a>
                </div>
                
                <!-- Pro -->
                <div class="bg-darkest border-2 border-wall-blue rounded-2xl p-8 relative">
                    <div class="absolute -top-4 left-1/2 -translate-x-1/2 bg-wall-blue text-white text-sm font-semibold px-4 py-1 rounded-full">
                        Most Popular
                    </div>
                    <h3 class="text-xl font-bold mb-2 text-white">Pro</h3>
                    <div class="text-4xl font-bold text-white mb-1">$49</div>
                    <div class="text-gray-400 mb-6">per month</div>
                    <ul class="space-y-3 mb-8">
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-wall-blue-light flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            50,000 requests/month
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-wall-blue-light flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            Advanced loop detection
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-wall-blue-light flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            Run-level budgets
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-wall-blue-light flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            Slack/Webhook alerts
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-wall-blue-light flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            30-day log retention
                        </li>
                    </ul>
                    <a href="#waitlist" class="block text-center gradient-bg hover:opacity-90 text-white px-6 py-3 rounded-xl font-semibold transition">
                        Get Started
                    </a>
                </div>
                
                <!-- Enterprise -->
                <div class="bg-lighter border border-gray-200 rounded-2xl p-8">
                    <h3 class="text-xl font-bold mb-2 text-darkest">Enterprise</h3>
                    <div class="text-4xl font-bold text-darkest mb-1">Custom</div>
                    <div class="text-gray-500 mb-6">Contact us</div>
                    <ul class="space-y-3 mb-8">
                        <li class="flex items-center gap-3 text-gray-600">
                            <svg class="w-5 h-5 text-success-green flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            Unlimited requests
                        </li>
                        <li class="flex items-center gap-3 text-gray-600">
                            <svg class="w-5 h-5 text-success-green flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            Self-host option
                        </li>
                        <li class="flex items-center gap-3 text-gray-600">
                            <svg class="w-5 h-5 text-success-green flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            Zero retention mode
                        </li>
                        <li class="flex items-center gap-3 text-gray-600">
                            <svg class="w-5 h-5 text-success-green flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            SSO & RBAC
                        </li>
                        <li class="flex items-center gap-3 text-gray-600">
                            <svg class="w-5 h-5 text-success-green flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                            </svg>
                            Dedicated support
                        </li>
                    </ul>
                    <a href="mailto:enterprise@agentwall.io" class="block text-center border-2 border-gray-300 hover:border-wall-blue text-dark hover:text-wall-blue px-6 py-3 rounded-xl font-semibold transition">
                        Contact Sales
                    </a>
                </div>
            </div>
        </div>
    </section>


    <!-- Waitlist Section -->
    <section id="waitlist" class="py-20 px-4 bg-lighter">
        <div class="max-w-2xl mx-auto text-center">
            <div class="w-20 h-20 gradient-bg rounded-2xl flex items-center justify-center mx-auto mb-6">
                <img src="/branding/logo-icon.svg" alt="AgentWall" class="h-12 w-12">
            </div>
            <h2 class="text-3xl md:text-4xl font-bold mb-4 text-darkest">Get Early Access</h2>
            <p class="text-xl text-gray-600 mb-8">Join the waitlist and be the first to guard your agents.</p>
            
            <form class="flex flex-col sm:flex-row gap-4 max-w-md mx-auto" x-data="{ email: '', submitted: false, loading: false }" @submit.prevent="loading = true; setTimeout(() => { submitted = true; loading = false; }, 800)">
                <input 
                    type="email" 
                    x-model="email"
                    placeholder="you@company.com" 
                    class="flex-1 px-6 py-4 rounded-xl bg-white border-2 border-gray-200 focus:border-wall-blue focus:outline-none font-medium"
                    required
                    x-show="!submitted"
                >
                <button 
                    type="submit" 
                    class="gradient-bg hover:opacity-90 text-white px-8 py-4 rounded-xl font-semibold transition flex items-center justify-center gap-2"
                    x-show="!submitted"
                    :disabled="loading"
                >
                    <span x-show="!loading">Join Waitlist</span>
                    <span x-show="loading" class="flex items-center gap-2">
                        <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                        </svg>
                        Joining...
                    </span>
                </button>
                <div x-show="submitted" x-transition class="bg-success-green/10 border border-success-green/30 rounded-xl p-6">
                    <div class="flex items-center justify-center gap-3 text-success-green">
                        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                        </svg>
                        <span class="text-lg font-semibold">You're on the list!</span>
                    </div>
                    <p class="text-gray-600 mt-2">We'll be in touch soon.</p>
                </div>
            </form>
            
            <p class="text-gray-500 text-sm mt-6">No spam. Just product updates.</p>
        </div>
    </section>

    <!-- Footer -->
    <footer class="py-12 px-4 bg-darkest text-white">
        <div class="max-w-7xl mx-auto">
            <div class="grid md:grid-cols-4 gap-8 mb-12">
                <!-- Brand -->
                <div class="md:col-span-2">
                    <a href="/" class="flex items-center mb-4">
                        <img src="/branding/logo-dark.svg" alt="AgentWall" class="h-10 w-auto">
                    </a>
                    <p class="text-gray-400 mb-4 max-w-sm">The first Agent Firewall for AI. Guard the Agent, Save the Budget.</p>
                    <div class="flex items-center gap-4">
                        <a href="https://twitter.com/agentwall" class="text-gray-400 hover:text-white transition">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                            </svg>
                        </a>
                        <a href="https://github.com/agentwall" class="text-gray-400 hover:text-white transition">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"/>
                            </svg>
                        </a>
                        <a href="https://discord.gg/agentwall" class="text-gray-400 hover:text-white transition">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189z"/>
                            </svg>
                        </a>
                    </div>
                </div>
                
                <!-- Links -->
                <div>
                    <h4 class="font-semibold mb-4">Product</h4>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="#features" class="hover:text-white transition">Features</a></li>
                        <li><a href="#pricing" class="hover:text-white transition">Pricing</a></li>
                        <li><a href="https://docs.agentwall.io" class="hover:text-white transition">Documentation</a></li>
                        <li><a href="https://status.agentwall.io" class="hover:text-white transition">Status</a></li>
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
                <div class="text-gray-500 text-sm mb-4 md:mb-0">
                    © 2026 AgentWall. All rights reserved.
                </div>
                <div class="text-gray-500 text-sm">
                    Guard the Agent, Save the Budget 🛡️
                </div>
            </div>
        </div>
    </footer>
</body>
</html><?php /**PATH C:\wamp64\www\AgentGuardProjesi\laravel\resources\views/welcome.blade.php ENDPATH**/ ?>