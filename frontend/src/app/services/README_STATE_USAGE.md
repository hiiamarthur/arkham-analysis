# Using Global App State

This guide explains how to use the global application state service to access cached metadata (traits, encounter sets, etc.).

## Quick Start

### 1. Inject the AppStateService

```typescript
import { Component, computed } from '@angular/core';
import { AppStateService } from '../services/app-state.service';

@Component({
  selector: 'app-my-component',
  standalone: true,
  // ...
})
export class MyComponent {
  constructor(private appState: AppStateService) {}
}
```

### 2. Access Cached Data

The service exposes reactive signals that you can use directly in your templates or computed values:

```typescript
export class MyComponent {
  constructor(private appState: AppStateService) {}

  // Access traits
  allTraits = this.appState.traits;

  // Access encounter sets
  allEncounterSets = this.appState.encounterSets;

  // Check if data is loading
  isLoading = this.appState.isLoading;

  // Check if cache is valid
  isCacheValid = this.appState.isCacheValid;

  // Get last update timestamp
  lastUpdated = this.appState.lastUpdated;

  // Example: Create a computed value
  traitCount = computed(() => this.allTraits().length);

  // Example: Filter traits
  weaponTraits = computed(() =>
    this.allTraits().filter(t => t.toLowerCase().includes('weapon'))
  );
}
```

### 3. Use in Templates

```html
<!-- Display all traits -->
<select>
  <option value="">Select a trait...</option>
  <option *ngFor="let trait of allTraits()" [value]="trait">
    {{trait}}
  </option>
</select>

<!-- Display encounter sets -->
<div *ngFor="let encounterSet of allEncounterSets()">
  <span>{{encounterSet.name}} ({{encounterSet.code}})</span>
</div>

<!-- Show loading state -->
<div *ngIf="isLoading()">Loading metadata...</div>

<!-- Show cache status -->
<div>
  Cache valid: {{isCacheValid() ? 'Yes' : 'No'}}
  Last updated: {{lastUpdated() | date:'short'}}
</div>
```

## Advanced Usage

### Manual Refresh

If you need to force refresh the metadata:

```typescript
import { MetadataService } from '../services/metadata.service';

export class MyComponent {
  constructor(
    private appState: AppStateService,
    private metadataService: MetadataService
  ) {}

  refreshData() {
    this.metadataService.refreshMetadata().subscribe({
      next: () => console.log('Metadata refreshed'),
      error: (err) => console.error('Refresh failed:', err)
    });
  }
}
```

### Clear Cache

To clear all cached data:

```typescript
clearCache() {
  this.appState.clearCache();
}
```

### Invalidate Cache

To mark cache as invalid without clearing it:

```typescript
invalidateCache() {
  this.appState.invalidateCache();
}
```

## How It Works

1. **Automatic Loading**: When the app starts, metadata is automatically loaded from the API or localStorage
2. **Caching**: Data is cached in localStorage for 24 hours
3. **Reactive Updates**: All data is exposed as signals, so your UI updates automatically
4. **Persistence**: Changes are automatically saved to localStorage

## Data Structure

### Traits
```typescript
traits: string[]  // Array of unique trait names
// Example: ['Item', 'Weapon', 'Firearm', 'Spell', ...]
```

### Encounter Sets
```typescript
encounterSets: EncounterSet[]

interface EncounterSet {
  code: string;  // Unique code like 'torch'
  name: string;  // Display name like 'The Gathering'
}
```

## Best Practices

1. **Use Signals**: Always access data through the signal methods (e.g., `traits()` not `traits`)
2. **Computed Values**: Use `computed()` for derived state instead of methods
3. **Avoid Manual Updates**: Let the MetadataService handle updates
4. **Check Loading State**: Show loading indicators when `isLoading()` is true

## Example: Complete Component

```typescript
import { Component, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AppStateService } from '../services/app-state.service';
import { MetadataService } from '../services/metadata.service';

@Component({
  selector: 'app-trait-selector',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div>
      <h3>Select Trait</h3>

      <div *ngIf="isLoading()">Loading traits...</div>

      <select [(ngModel)]="selectedTrait" *ngIf="!isLoading()">
        <option value="">Select...</option>
        <option *ngFor="let trait of sortedTraits()" [value]="trait">
          {{trait}}
        </option>
      </select>

      <p>Total traits: {{traitCount()}}</p>
      <p>Cache valid: {{isCacheValid() ? 'Yes' : 'No'}}</p>

      <button (click)="refresh()">Refresh Data</button>
    </div>
  `
})
export class TraitSelectorComponent {
  selectedTrait = '';

  constructor(
    private appState: AppStateService,
    private metadataService: MetadataService
  ) {}

  // Reactive state from app state
  isLoading = this.appState.isLoading;
  isCacheValid = this.appState.isCacheValid;
  allTraits = this.appState.traits;

  // Computed values
  traitCount = computed(() => this.allTraits().length);
  sortedTraits = computed(() =>
    [...this.allTraits()].sort((a, b) => a.localeCompare(b))
  );

  refresh() {
    this.metadataService.refreshMetadata().subscribe();
  }
}
```
