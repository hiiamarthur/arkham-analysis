import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, forkJoin, of } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { AppStateService, EncounterSet, Investigator } from './app-state.service';

/**
 * Service for fetching and caching application metadata
 * (traits, encounter sets, investigators, etc.)
 */
@Injectable({
  providedIn: 'root'
})
export class MetadataService {
  private apiUrl = `${environment.apiUrl}/cards/metadata`;

  constructor(
    private http: HttpClient,
    private appState: AppStateService
  ) {}

  /**
   * Fetch all traits from API
   */
  fetchTraits(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/traits`).pipe(
      tap(traits => {
        this.appState.setTraits(traits);
      }),
      catchError(error => {
        console.error('Error fetching traits:', error);
        return of([]);
      })
    );
  }

  /**
   * Fetch all encounter sets from API
   */
  fetchEncounterSets(): Observable<EncounterSet[]> {
    return this.http.get<EncounterSet[]>(`${this.apiUrl}/encounter_sets`).pipe(
      tap(encounterSets => {
        this.appState.setEncounterSets(encounterSets);
      }),
      catchError(error => {
        console.error('Error fetching encounter sets:', error);
        return of([]);
      })
    );
  }

  /**
   * Fetch all investigators from API
   */
  fetchInvestigators(): Observable<Investigator[]> {
    return this.http.get<Investigator[]>(`${this.apiUrl}/investigators`).pipe(
      tap(investigators => {
        this.appState.setInvestigators(investigators);
      }),
      catchError(error => {
        console.error('Error fetching investigators:', error);
        return of([]);
      })
    );
  }

  /**
   * Fetch all metadata at once
   * Returns an observable that completes when all requests finish
   */
  fetchAllMetadata(): Observable<{
    traits: string[];
    encounterSets: EncounterSet[];
    investigators: Investigator[];
  }> {
    this.appState.setLoading(true);

    return forkJoin({
      traits: this.fetchTraits(),
      encounterSets: this.fetchEncounterSets(),
      investigators: this.fetchInvestigators()
    }).pipe(
      tap(() => {
        this.appState.setLoading(false);
      }),
      catchError(error => {
        console.error('Error fetching metadata:', error);
        this.appState.setLoading(false);
        return of({ traits: [], encounterSets: [], investigators: [] });
      })
    );
  }

  /**
   * Initialize metadata - fetches from API only if cache is invalid
   */
  initializeMetadata(): Observable<any> {
    // Check if cache is still valid
    if (this.appState.isCacheValid()) {
      console.log('Using cached metadata');
      return of(null); // Return immediately, cache is valid
    }

    console.log('Fetching fresh metadata from API');
    return this.fetchAllMetadata();
  }

  /**
   * Force refresh all metadata from API
   */
  refreshMetadata(): Observable<any> {
    this.appState.invalidateCache();
    return this.fetchAllMetadata();
  }
}
