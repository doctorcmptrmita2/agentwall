<?php

namespace App\Data;

class BlogPosts
{
    public static function getImageUrls(): array
    {
        return [
            'protecting-ai-agents-from-prompt-injection' => 'https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=1200&h=600&fit=crop',
            'data-loss-prevention-for-llm-applications' => 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1200&h=600&fit=crop',
            'securing-api-keys-in-ai-agent-workflows' => 'https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=1200&h=600&fit=crop',
            'zero-trust-architecture-for-ai-agents' => 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&h=600&fit=crop',
            'audit-trails-for-ai-compliance' => 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1200&h=600&fit=crop',
            'preventing-50k-surprise-ai-bills' => 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1200&h=600&fit=crop',
            'run-level-budgets-explained' => 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1200&h=600&fit=crop',
            'optimizing-token-usage-in-ai-agents' => 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=600&fit=crop',
            'real-time-cost-monitoring-for-ai' => 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=600&fit=crop',
            'ai-cost-allocation-for-teams' => 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&h=600&fit=crop',
            'what-is-agent-governance' => 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&h=600&fit=crop',
            'detecting-infinite-loops-in-ai-agents' => 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=1200&h=600&fit=crop',
            'run-level-tracking-vs-request-tracking' => 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=600&fit=crop',
            'tool-governance-for-ai-agents' => 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1200&h=600&fit=crop',
            'building-observable-ai-agents' => 'https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1200&h=600&fit=crop',
            'anomaly-detection-in-agent-behavior' => 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=600&fit=crop',
            'introducing-agentwall' => 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&h=600&fit=crop',
            'agentwall-kill-switch-feature' => 'https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=1200&h=600&fit=crop',
            'getting-started-with-agentwall' => 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&h=600&fit=crop',
            'agentwall-enterprise-features' => 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=1200&h=600&fit=crop',
        ];
    }

    public static function getFaqs(): array
    {
        return [
            'protecting-ai-agents-from-prompt-injection' => [
                ['q' => 'Can prompt injection be completely prevented?', 'a' => 'No security measure is 100% effective. However, layered defenses can reduce the risk to acceptable levels. The goal is to make attacks difficult, detectable, and limited in impact.'],
                ['q' => 'How do I test my agents for injection vulnerabilities?', 'a' => 'Use red team exercises with security professionals who attempt to compromise your agents. Automated testing tools can also help identify common vulnerabilities.'],
                ['q' => 'Are some AI models more resistant to injection?', 'a' => 'Model architecture and training can affect injection resistance, but no model is immune. Security must be implemented at the application layer regardless of which AI model you use.'],
                ['q' => 'What is the performance impact of injection protection?', 'a' => 'Well-implemented protection adds minimal latency. AgentWall maintains less than 10ms overhead while providing comprehensive security scanning.'],
            ],
            'data-loss-prevention-for-llm-applications' => [
                ['q' => 'Does DLP slow down AI agent responses?', 'a' => 'Well-implemented DLP adds minimal latency—typically under 10ms. The key is efficient pattern matching and parallel processing of security checks.'],
                ['q' => 'How do I handle false positives?', 'a' => 'Tune your DLP rules based on observed false positive rates. Consider implementing a review queue for borderline cases rather than blocking all potential matches.'],
                ['q' => 'Can users bypass DLP controls?', 'a' => 'Determined users might attempt to encode sensitive data to evade detection. Defense in depth, including output monitoring and anomaly detection, helps catch bypass attempts.'],
                ['q' => 'What types of data should I protect?', 'a' => 'Focus on PII (names, SSNs, emails), financial data (credit cards, bank accounts), and intellectual property (trade secrets, proprietary algorithms).'],
            ],
            'securing-api-keys-in-ai-agent-workflows' => [
                ['q' => 'How often should I rotate API keys?', 'a' => 'Best practice is to rotate keys at least every 90 days, or immediately if there\'s any suspicion of compromise. Automated rotation can make more frequent rotation practical.'],
                ['q' => 'What if I accidentally commit a key to Git?', 'a' => 'Immediately revoke the key and generate a new one. The old key should be considered compromised even if you remove it from the repository, as it may exist in Git history.'],
                ['q' => 'Should I use different keys for dev and production?', 'a' => 'Absolutely. Always use separate keys for different environments. This isolation limits the blast radius if a development key is compromised.'],
            ],
            'preventing-50k-surprise-ai-bills' => [
                ['q' => 'How quickly can costs spiral out of control?', 'a' => 'A single infinite loop can rack up thousands of dollars in hours. Without proper controls, a runaway agent can exhaust your monthly budget overnight.'],
                ['q' => 'What\'s the difference between request-level and run-level budgets?', 'a' => 'Request-level budgets only limit individual API calls. Run-level budgets track the entire agent task from start to finish, catching loops that span multiple requests.'],
                ['q' => 'Can I set different budgets for different agents?', 'a' => 'Yes, AgentWall allows per-agent, per-team, and per-project budget controls with automatic enforcement and alerts.'],
            ],
            'detecting-infinite-loops-in-ai-agents' => [
                ['q' => 'How does loop detection work?', 'a' => 'AgentWall tracks prompt similarity, output patterns, and step counts across a run. When repetition exceeds thresholds, the system automatically flags or terminates the run.'],
                ['q' => 'Will loop detection stop legitimate retries?', 'a' => 'No. The system distinguishes between intentional retries (with backoff) and pathological loops. You can configure sensitivity to match your use case.'],
                ['q' => 'Can I manually override the kill switch?', 'a' => 'Yes, authorized users can manually trigger or override the kill switch from the dashboard. All actions are logged for audit purposes.'],
            ],
        ];
    }
    
    public static function getDefaultFaqs(): array
    {
        return [
            ['q' => 'How does AgentWall help with this?', 'a' => 'AgentWall provides comprehensive governance controls with less than 10ms latency overhead. Our platform combines security, cost management, and operational visibility in a single solution.'],
            ['q' => 'Is this suitable for production environments?', 'a' => 'Yes, AgentWall is designed for production use with 99.9% uptime SLA. Our architecture ensures minimal performance impact while providing enterprise-grade security and monitoring.'],
            ['q' => 'Can I customize the policies?', 'a' => 'Absolutely. AgentWall offers flexible policy configuration that can be tailored to your specific requirements. Set custom thresholds, rules, and alerts based on your operational needs.'],
            ['q' => 'What about compliance requirements?', 'a' => 'AgentWall maintains comprehensive audit trails and supports compliance with major regulations including GDPR, SOC 2, and industry-specific requirements. All agent actions are logged for regulatory review.'],
        ];
    }

    public static function getCategories(): array
    {
        return [
            'ai-security' => [
                'name' => 'AI Security',
                'color' => 'wall-blue',
                'icon' => 'shield',
            ],
            'cost-control' => [
                'name' => 'Cost Control',
                'color' => 'success-green',
                'icon' => 'dollar',
            ],
            'agent-governance' => [
                'name' => 'Agent Governance',
                'color' => 'warning-orange',
                'icon' => 'cog',
            ],
            'product-updates' => [
                'name' => 'Product Updates',
                'color' => 'purple-500',
                'icon' => 'sparkles',
            ],
        ];
    }

    public static function getTags(): array
    {
        return [
            'loop-detection', 'cost-optimization', 'security', 'dlp', 
            'prompt-injection', 'api-keys', 'budgets', 'monitoring',
            'kill-switch', 'run-tracking', 'openai', 'enterprise',
            'best-practices', 'tutorial', 'case-study', 'announcement'
        ];
    }

    public static function getPosts(): array
    {
        return [
            // AI Security (5 articles)
            [
                'id' => 1,
                'slug' => 'protecting-ai-agents-from-prompt-injection',
                'title' => 'Protecting AI Agents from Prompt Injection Attacks',
                'excerpt' => 'Learn how prompt injection attacks work and discover proven strategies to protect your AI agents from malicious inputs.',
                'category' => 'ai-security',
                'tags' => ['security', 'prompt-injection', 'best-practices'],
                'author' => 'AgentWall Team',
                'date' => '2026-01-05',
                'read_time' => 8,
                'featured' => true,
            ],
            [
                'id' => 2,
                'slug' => 'data-loss-prevention-for-llm-applications',
                'title' => 'Data Loss Prevention (DLP) for LLM Applications',
                'excerpt' => 'Implement robust DLP strategies to prevent sensitive data from leaking through your AI agent interactions.',
                'category' => 'ai-security',
                'tags' => ['dlp', 'security', 'enterprise'],
                'author' => 'AgentWall Team',
                'date' => '2026-01-04',
                'read_time' => 10,
                'featured' => false,
            ],
            [
                'id' => 3,
                'slug' => 'securing-api-keys-in-ai-agent-workflows',
                'title' => 'Securing API Keys in AI Agent Workflows',
                'excerpt' => 'Best practices for managing and protecting API keys when building autonomous AI agent systems.',
                'category' => 'ai-security',
                'tags' => ['api-keys', 'security', 'best-practices'],
                'author' => 'AgentWall Team',
                'date' => '2026-01-03',
                'read_time' => 7,
                'featured' => false,
            ],
            [
                'id' => 4,
                'slug' => 'zero-trust-architecture-for-ai-agents',
                'title' => 'Zero Trust Architecture for AI Agents',
                'excerpt' => 'Why zero trust principles are essential for AI agent security and how to implement them effectively.',
                'category' => 'ai-security',
                'tags' => ['security', 'enterprise', 'best-practices'],
                'author' => 'AgentWall Team',
                'date' => '2026-01-02',
                'read_time' => 9,
                'featured' => false,
            ],
            [
                'id' => 5,
                'slug' => 'audit-trails-for-ai-compliance',
                'title' => 'Building Audit Trails for AI Compliance',
                'excerpt' => 'How to create comprehensive audit trails that satisfy regulatory requirements for AI systems.',
                'category' => 'ai-security',
                'tags' => ['security', 'enterprise', 'monitoring'],
                'author' => 'AgentWall Team',
                'date' => '2026-01-01',
                'read_time' => 8,
                'featured' => false,
            ],

            // Cost Control (5 articles)
            [
                'id' => 6,
                'slug' => 'preventing-50k-surprise-ai-bills',
                'title' => 'How to Prevent $50K Surprise AI Bills',
                'excerpt' => 'Real strategies to avoid unexpected costs from runaway AI agents and infinite loops.',
                'category' => 'cost-control',
                'tags' => ['cost-optimization', 'budgets', 'best-practices'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-30',
                'read_time' => 7,
                'featured' => true,
            ],
            [
                'id' => 7,
                'slug' => 'run-level-budgets-explained',
                'title' => 'Run-Level Budgets: The Key to AI Cost Control',
                'excerpt' => 'Why per-request budgets fail and how run-level budgets provide true cost governance.',
                'category' => 'cost-control',
                'tags' => ['budgets', 'run-tracking', 'cost-optimization'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-28',
                'read_time' => 9,
                'featured' => false,
            ],
            [
                'id' => 8,
                'slug' => 'optimizing-token-usage-in-ai-agents',
                'title' => 'Optimizing Token Usage in AI Agents',
                'excerpt' => 'Practical techniques to reduce token consumption without sacrificing agent performance.',
                'category' => 'cost-control',
                'tags' => ['cost-optimization', 'openai', 'best-practices'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-26',
                'read_time' => 8,
                'featured' => false,
            ],
            [
                'id' => 9,
                'slug' => 'real-time-cost-monitoring-for-ai',
                'title' => 'Real-Time Cost Monitoring for AI Applications',
                'excerpt' => 'Set up effective cost monitoring dashboards to track AI spending as it happens.',
                'category' => 'cost-control',
                'tags' => ['monitoring', 'cost-optimization', 'tutorial'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-24',
                'read_time' => 6,
                'featured' => false,
            ],
            [
                'id' => 10,
                'slug' => 'ai-cost-allocation-for-teams',
                'title' => 'AI Cost Allocation Strategies for Teams',
                'excerpt' => 'How to fairly allocate AI costs across teams and projects in your organization.',
                'category' => 'cost-control',
                'tags' => ['budgets', 'enterprise', 'best-practices'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-22',
                'read_time' => 7,
                'featured' => false,
            ],

            // Agent Governance (6 articles)
            [
                'id' => 11,
                'slug' => 'what-is-agent-governance',
                'title' => 'What is Agent Governance and Why It Matters',
                'excerpt' => 'Understanding the emerging field of AI agent governance and its importance for enterprise adoption.',
                'category' => 'agent-governance',
                'tags' => ['best-practices', 'enterprise', 'monitoring'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-20',
                'read_time' => 10,
                'featured' => true,
            ],
            [
                'id' => 12,
                'slug' => 'detecting-infinite-loops-in-ai-agents',
                'title' => 'Detecting and Stopping Infinite Loops in AI Agents',
                'excerpt' => 'Technical deep-dive into loop detection algorithms and automatic kill switches.',
                'category' => 'agent-governance',
                'tags' => ['loop-detection', 'kill-switch', 'tutorial'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-18',
                'read_time' => 11,
                'featured' => false,
            ],
            [
                'id' => 13,
                'slug' => 'run-level-tracking-vs-request-tracking',
                'title' => 'Run-Level Tracking vs Request Tracking: A Comparison',
                'excerpt' => 'Why tracking entire agent runs provides better insights than individual request logging.',
                'category' => 'agent-governance',
                'tags' => ['run-tracking', 'monitoring', 'best-practices'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-16',
                'read_time' => 8,
                'featured' => false,
            ],
            [
                'id' => 14,
                'slug' => 'tool-governance-for-ai-agents',
                'title' => 'Tool Governance: Controlling What Your Agents Can Do',
                'excerpt' => 'Implement fine-grained control over which tools and APIs your AI agents can access.',
                'category' => 'agent-governance',
                'tags' => ['security', 'best-practices', 'enterprise'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-14',
                'read_time' => 9,
                'featured' => false,
            ],
            [
                'id' => 15,
                'slug' => 'building-observable-ai-agents',
                'title' => 'Building Observable AI Agents',
                'excerpt' => 'Best practices for adding observability to your AI agents for debugging and monitoring.',
                'category' => 'agent-governance',
                'tags' => ['monitoring', 'tutorial', 'best-practices'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-12',
                'read_time' => 8,
                'featured' => false,
            ],
            [
                'id' => 16,
                'slug' => 'anomaly-detection-in-agent-behavior',
                'title' => 'Anomaly Detection in AI Agent Behavior',
                'excerpt' => 'How to identify unusual patterns in agent behavior before they become costly problems.',
                'category' => 'agent-governance',
                'tags' => ['monitoring', 'loop-detection', 'security'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-10',
                'read_time' => 9,
                'featured' => false,
            ],

            // Product Updates (4 articles)
            [
                'id' => 17,
                'slug' => 'introducing-agentwall',
                'title' => 'Introducing AgentWall: The First Agent Firewall',
                'excerpt' => 'Meet AgentWall - the control layer that AI agents need. Guard the Agent, Save the Budget.',
                'category' => 'product-updates',
                'tags' => ['announcement', 'tutorial'],
                'author' => 'AgentWall Team',
                'date' => '2026-01-05',
                'read_time' => 6,
                'featured' => true,
            ],
            [
                'id' => 18,
                'slug' => 'agentwall-kill-switch-feature',
                'title' => 'New Feature: Instant Kill Switch for Runaway Agents',
                'excerpt' => 'Stop any agent run instantly with our new kill switch feature. Never lose control again.',
                'category' => 'product-updates',
                'tags' => ['announcement', 'kill-switch'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-28',
                'read_time' => 5,
                'featured' => false,
            ],
            [
                'id' => 19,
                'slug' => 'getting-started-with-agentwall',
                'title' => 'Getting Started with AgentWall in 5 Minutes',
                'excerpt' => 'A quick guide to integrating AgentWall with your existing AI agent infrastructure.',
                'category' => 'product-updates',
                'tags' => ['tutorial', 'openai'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-20',
                'read_time' => 5,
                'featured' => false,
            ],
            [
                'id' => 20,
                'slug' => 'agentwall-enterprise-features',
                'title' => 'AgentWall Enterprise: Self-Host & Zero Retention',
                'excerpt' => 'Announcing enterprise features including self-hosting and zero retention mode for maximum privacy.',
                'category' => 'product-updates',
                'tags' => ['announcement', 'enterprise', 'security'],
                'author' => 'AgentWall Team',
                'date' => '2025-12-15',
                'read_time' => 6,
                'featured' => false,
            ],
        ];
    }

    public static function getPost(string $slug): ?array
    {
        $posts = self::getPosts();
        foreach ($posts as $post) {
            if ($post['slug'] === $slug) {
                return $post;
            }
        }
        return null;
    }

    public static function getFeaturedPosts(): array
    {
        return array_filter(self::getPosts(), fn($p) => $p['featured']);
    }

    public static function getPostsByCategory(string $category): array
    {
        return array_filter(self::getPosts(), fn($p) => $p['category'] === $category);
    }

    public static function getPostsByTag(string $tag): array
    {
        return array_filter(self::getPosts(), fn($p) => in_array($tag, $p['tags']));
    }
}
