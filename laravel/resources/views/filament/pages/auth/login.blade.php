<x-filament-panels::page.simple>
    @if (filament()->hasLogin())
        <x-slot name="heading">
            <div class="flex flex-col items-center gap-4 mb-6">
                {{-- Logo --}}
                <div class="flex items-center gap-3">
                    <div class="flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 shadow-lg">
                        <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                        </svg>
                    </div>
                    <div>
                        <h1 class="text-3xl font-bold tracking-tight text-gray-950 dark:text-white">
                            <span>Agent</span><span class="text-primary-600 dark:text-primary-400">Wall</span>
                        </h1>
                    </div>
                </div>
                
                {{-- Tagline --}}
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Guard the Agent, Save the Budget
                </p>
            </div>
        </x-slot>
    @endif

    {{ $this->form }}

    <x-filament-panels::form.actions
        :actions="$this->getCachedFormActions()"
        :full-width="$this->hasFullWidthFormActions()"
    />
</x-filament-panels::page.simple>
