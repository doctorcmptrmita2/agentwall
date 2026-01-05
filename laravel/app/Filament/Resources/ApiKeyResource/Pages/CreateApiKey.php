<?php

namespace App\Filament\Resources\ApiKeyResource\Pages;

use App\Filament\Resources\ApiKeyResource;
use App\Models\ApiKey;
use Filament\Resources\Pages\CreateRecord;
use Filament\Notifications\Notification;

class CreateApiKey extends CreateRecord
{
    protected static string $resource = ApiKeyResource::class;
    
    protected ?string $generatedKey = null;

    protected function mutateFormDataBeforeCreate(array $data): array
    {
        $keyData = ApiKey::generateKey();
        
        $data['key_prefix'] = $keyData['prefix'];
        $data['key_hash'] = $keyData['hash'];
        
        $this->generatedKey = $keyData['key'];
        
        return $data;
    }

    protected function afterCreate(): void
    {
        Notification::make()
            ->title('API Key Created Successfully!')
            ->body('Your new API key: ' . $this->generatedKey)
            ->success()
            ->persistent()
            ->actions([
                \Filament\Notifications\Actions\Action::make('copy')
                    ->button()
                    ->label('Copy Key')
                    ->url('#')
                    ->extraAttributes([
                        'onclick' => "navigator.clipboard.writeText('{$this->generatedKey}'); return false;",
                    ]),
            ])
            ->send();
    }
}
