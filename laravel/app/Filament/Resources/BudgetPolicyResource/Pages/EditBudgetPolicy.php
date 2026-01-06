<?php

namespace App\Filament\Resources\BudgetPolicyResource\Pages;

use App\Filament\Resources\BudgetPolicyResource;
use Filament\Actions;
use Filament\Resources\Pages\EditRecord;

class EditBudgetPolicy extends EditRecord
{
    protected static string $resource = BudgetPolicyResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\DeleteAction::make(),
        ];
    }

    protected function getRedirectUrl(): string
    {
        return $this->getResource()::getUrl('index');
    }
}
