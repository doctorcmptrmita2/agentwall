<?php

namespace Database\Seeders;

use App\Models\Team;
use App\Models\ApiKey;
use App\Models\AgentRun;
use App\Models\Article;
use App\Data\BlogPosts;
use Illuminate\Database\Seeder;

class DemoSeeder extends Seeder
{
    public function run(): void
    {
        // Create demo team
        $team = Team::firstOrCreate(
            ['slug' => 'demo-team'],
            [
                'name' => 'Demo Team',
                'daily_budget' => 10.00,
                'monthly_budget' => 100.00,
            ]
        );

        // Create demo API key
        $keyData = ApiKey::generateKey();
        ApiKey::firstOrCreate(
            ['name' => 'Demo Key'],
            [
                'team_id' => $team->id,
                'name' => 'Demo Key',
                'key_prefix' => $keyData['prefix'],
                'key_hash' => $keyData['hash'],
                'is_active' => true,
            ]
        );

        // Create demo runs
        AgentRun::firstOrCreate(['run_id' => 'demo-run-001'], [
            'team_id' => $team->id,
            'model' => 'gpt-4o-mini',
            'step_count' => 5,
            'total_tokens' => 1500,
            'total_cost' => 0.0025,
            'status' => 'running',
            'started_at' => now(),
        ]);

        AgentRun::firstOrCreate(['run_id' => 'demo-run-002'], [
            'team_id' => $team->id,
            'model' => 'gpt-4o',
            'step_count' => 12,
            'total_tokens' => 5000,
            'total_cost' => 0.05,
            'status' => 'killed',
            'kill_reason' => 'loop_detected',
            'loop_detected' => true,
            'started_at' => now()->subMinutes(30),
            'ended_at' => now()->subMinutes(25),
        ]);


        // Seed blog articles
        $posts = BlogPosts::getPosts();
        $imageUrls = BlogPosts::getImageUrls();
        
        $defaultContent = '<p class="text-xl text-gray-600 leading-relaxed mb-8">Understanding this topic is crucial for effective AI agent governance and security.</p>

<h2>Overview</h2>
<p>As AI agents become more prevalent, implementing proper controls and monitoring is essential for maintaining security and controlling costs.</p>

<h2>Key Challenges</h2>
<ul class="list-disc pl-6 space-y-2 my-4">
    <li><strong>Security:</strong> Protecting against unauthorized access and data leaks</li>
    <li><strong>Cost Control:</strong> Preventing runaway spending</li>
    <li><strong>Visibility:</strong> Real-time monitoring of agent behavior</li>
</ul>

<h2>Best Practices</h2>
<p>AgentWall provides comprehensive governance with less than 10ms latency overhead.</p>

<h2>Conclusion</h2>
<p>Effective governance is essential for safe AI agent operations.</p>';

        $defaultFaqs = [
            ['q' => 'How does AgentWall help?', 'a' => 'AgentWall provides comprehensive governance with <10ms latency overhead.'],
            ['q' => 'Is this production-ready?', 'a' => 'Yes, designed for production with 99.9% uptime SLA.'],
            ['q' => 'Can I customize policies?', 'a' => 'Absolutely. Flexible configuration tailored to your needs.'],
            ['q' => 'What about compliance?', 'a' => 'Comprehensive audit trails supporting GDPR, SOC 2, and more.'],
        ];
        
        foreach ($posts as $post) {
            Article::updateOrCreate(
                ['slug' => $post['slug']],
                [
                    'title' => $post['title'],
                    'excerpt' => $post['excerpt'],
                    'image_url' => $imageUrls[$post['slug']] ?? null,
                    'content' => $defaultContent,
                    'faqs' => $defaultFaqs,
                    'category' => $post['category'],
                    'tags' => $post['tags'],
                    'author' => $post['author'],
                    'date' => $post['date'],
                    'read_time' => $post['read_time'],
                    'featured' => $post['featured'],
                ]
            );
        }

        $this->command->info('Demo data seeded successfully!');
        $this->command->info('Seeded ' . count($posts) . ' blog articles.');
    }
}
