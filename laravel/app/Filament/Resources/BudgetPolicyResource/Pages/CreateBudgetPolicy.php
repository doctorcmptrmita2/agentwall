<?php

namespace App\Filament\Resources\BudgetPolicyResource\Pages;

use App\Filament\Resources\BudgetPolicyResource;
use Filament\Resources\Pages\CreateRecord;

class CreateBudgetPolicy extends CreateRecord
{
    protected static string $resource = BudgetPolicyResource::class;

    protected function getRedirectUrl(): string
    {
        return $this->getResource()::getUrl('index');
    }
}
