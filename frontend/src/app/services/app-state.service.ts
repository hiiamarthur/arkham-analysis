import { Injectable, signal, computed, effect, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

/**
 * Encounter Set metadata
 */
export interface EncounterSet {
  code: string;
  name: string;
}

/**
 * Investigator metadata
 */
export interface Investigator {
  code: string;
  name: string;
  faction_code?: string;
}

/**
 * Application metadata cached globally
 */
export interface AppMetadata {
  version?: number;  // cache version
  traits: string[];
  encounterSets: EncounterSet[];
  investigators: Investigator[];
  lastUpdated: number;  // timestamp
}

/**
 * Global application state service with persistent storage.
 * Uses Angular signals for reactivity and localStorage for persistence.
 */
@Injectable({
  providedIn: 'root'
})
export class AppStateService {
  private readonly STORAGE_KEY = 'arkham_app_state';
  private readonly CACHE_VERSION = 2; // Increment this to invalidate old cache
  private readonly CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours in milliseconds
  private platformId = inject(PLATFORM_ID);

  // Signals for reactive state
  private _traits = signal<string[]>([]);
  private _encounterSets = signal<EncounterSet[]>([]);
  private _investigators = signal<Investigator[]>([]);
  private _lastUpdated = signal<number>(0);
  private _isLoading = signal<boolean>(false);

  // Public computed signals (read-only)
  readonly traits = computed(() => this._traits());
  readonly encounterSets = computed(() => this._encounterSets());
  readonly investigators = computed(() => this._investigators());
  readonly lastUpdated = computed(() => this._lastUpdated());
  readonly isLoading = computed(() => this._isLoading());
  readonly isCacheValid = computed(() => {
    const now = Date.now();
    const lastUpdate = this._lastUpdated();
    return lastUpdate > 0 && (now - lastUpdate) < this.CACHE_DURATION;
  });

  // Helper computed signal for investigator name lookup
  readonly investigatorMap = computed(() => {
    const map = new Map<string, string>();
    this._investigators().forEach(inv => map.set(inv.code, inv.name));
    return map;
  });

  constructor() {
    // Load initial state from localStorage
    this.loadFromLocalStorage();

    // Auto-save to localStorage whenever state changes
    effect(() => {
      this.saveToLocalStorage({
        version: this.CACHE_VERSION,
        traits: this._traits(),
        encounterSets: this._encounterSets(),
        investigators: this._investigators(),
        lastUpdated: this._lastUpdated()
      });
    });
  }

  /**
   * Load state from localStorage
   */
  private loadFromLocalStorage(): void {
    if (!isPlatformBrowser(this.platformId)) {
      return; // Skip localStorage access on server
    }

    try {
      const stored = localStorage.getItem(this.STORAGE_KEY);
      if (stored) {
        const metadata: AppMetadata = JSON.parse(stored);

        // Check cache version - if it doesn't match, clear cache
        if (!metadata.version || metadata.version !== this.CACHE_VERSION) {
          this.clearCache();
          return;
        }

        this._traits.set(metadata.traits || []);
        this._encounterSets.set(metadata.encounterSets || []);
        this._investigators.set(metadata.investigators || []);
        this._lastUpdated.set(metadata.lastUpdated || 0);
      }
    } catch (error) {
      console.error('Error loading app state from localStorage:', error);
    }
  }

  /**
   * Save state to localStorage
   */
  private saveToLocalStorage(metadata: AppMetadata): void {
    if (!isPlatformBrowser(this.platformId)) {
      return; // Skip localStorage access on server
    }

    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(metadata));
    } catch (error) {
      console.error('Error saving app state to localStorage:', error);
    }
  }

  /**
   * Update traits
   */
  setTraits(traits: string[]): void {
    this._traits.set(traits);
    this._lastUpdated.set(Date.now());
  }

  /**
   * Update encounter sets
   */
  setEncounterSets(encounterSets: EncounterSet[]): void {
    this._encounterSets.set(encounterSets);
    this._lastUpdated.set(Date.now());
  }

  /**
   * Update investigators
   */
  setInvestigators(investigators: Investigator[]): void {
    this._investigators.set(investigators);
    this._lastUpdated.set(Date.now());
  }

  /**
   * Update all metadata at once
   */
  setMetadata(metadata: Partial<AppMetadata>): void {
    if (metadata.traits) {
      this._traits.set(metadata.traits);
    }
    if (metadata.encounterSets) {
      this._encounterSets.set(metadata.encounterSets);
    }
    if (metadata.investigators) {
      this._investigators.set(metadata.investigators);
    }
    this._lastUpdated.set(Date.now());
  }

  /**
   * Set loading state
   */
  setLoading(isLoading: boolean): void {
    this._isLoading.set(isLoading);
  }

  /**
   * Clear all cached data
   */
  clearCache(): void {
    this._traits.set([]);
    this._encounterSets.set([]);
    this._investigators.set([]);
    this._lastUpdated.set(0);

    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(this.STORAGE_KEY);
    }
  }

  /**
   * Get investigator name by code
   */
  getInvestigatorName(code: string): string {
    return this.investigatorMap().get(code) || code;
  }

  /**
   * Force refresh (clears cache validity by setting lastUpdated to 0)
   */
  invalidateCache(): void {
    this._lastUpdated.set(0);
  }
}
