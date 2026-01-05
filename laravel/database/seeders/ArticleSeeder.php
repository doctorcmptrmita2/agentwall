<?php

namespace Database\Seeders;

use App\Models\Article;
use Illuminate\Database\Seeder;

class ArticleSeeder extends Seeder
{
    public function run(): void
    {
        $defaultContent = '<p class="text-xl text-gray-600 leading-relaxed mb-8">This article explores critical concepts in AI agent governance, security, and cost management.</p>

<h2>Overview</h2>
<p>As AI agents become more prevalent in enterprise environments, understanding these principles is crucial for maintaining security, controlling costs, and ensuring reliable operations.</p>

<h2>Key Challenges</h2>
<ul class="list-disc pl-6 space-y-2 my-4">
    <li><strong>Security Risks:</strong> Protecting against unauthorized access and data leaks</li>
    <li><strong>Cost Management:</strong> Preventing runaway spending from uncontrolled agent behavior</li>
    <li><strong>Operational Visibility:</strong> Monitoring and understanding agent actions in real-time</li>
    <li><strong>Compliance:</strong> Meeting regulatory requirements for AI system governance</li>
</ul>

<h2>Best Practices</h2>
<p>Implement comprehensive governance frameworks with AgentWall for complete control.</p>

<div class="bg-wall-blue/5 border-l-4 border-wall-blue rounded-r-xl p-6 my-8">
    <div class="flex items-start gap-3">
        <svg class="w-6 h-6 text-wall-blue flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <div>
            <h4 class="font-bold text-darkest mb-2">AgentWall Solution</h4>
            <p class="text-gray-600">AgentWall provides comprehensive governance with &lt;10ms latency overhead.</p>
        </div>
    </div>
</div>

<h2>Conclusion</h2>
<p>Effective AI agent governance is essential for safe, cost-effective operations.</p>';

        $defaultFaqs = [
            ['q' => 'How does AgentWall help with this?', 'a' => 'AgentWall provides comprehensive governance controls with less than 10ms latency overhead.'],
            ['q' => 'Is this suitable for production?', 'a' => 'Yes, AgentWall is designed for production use with 99.9% uptime SLA.'],
            ['q' => 'Can I customize the policies?', 'a' => 'Absolutely. AgentWall offers flexible policy configuration tailored to your needs.'],
            ['q' => 'What about compliance?', 'a' => 'AgentWall maintains comprehensive audit trails supporting GDPR, SOC 2, and more.'],
        ];

        $articles = [
