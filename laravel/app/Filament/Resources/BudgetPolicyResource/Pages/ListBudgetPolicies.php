<?php

namespace App\Filament\Resources\BudgetPolicyResource\Pages;

use App\Filament\Resources\BudgetPolicyResource;
use Filament\Actions;
use Filament\Resources\Pages\ListRecords;

class ListBudgetPolicies extends ListRecords
{
    protected static string $resource = BudgetPolicyResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\CreateAction::make(),
        ];
    }
}
