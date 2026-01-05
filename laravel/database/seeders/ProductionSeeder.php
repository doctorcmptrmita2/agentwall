<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class ProductionSeeder extends Seeder
{
    /**
     * Seed the application's database for production.
     */
    public function run(): void
    {
        // Seed all blog articles
        $this->call([
            ArticleBatch1Seeder::class,
            ArticleBatch2Seeder::class,
            ArticleBatch3Seeder::class,
            ArticleBatch4Seeder::class,
            ArticleBatch5Seeder::class,
            ArticleBatch6Seeder::class,
            ArticleBatch7Seeder::class,
        ]);

        $this->command->info('✅ Production data seeded successfully!');
        $this->command->info('📝 20 blog articles created');
    }
}
