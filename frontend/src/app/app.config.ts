import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection, APP_INITIALIZER } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { MetadataService } from './services/metadata.service';

/**
 * Initialize app metadata (traits, encounter sets) on app startup
 */
function initializeAppFactory(metadataService: MetadataService) {
  return () => metadataService.initializeMetadata().toPromise();
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(withFetch()),
    provideClientHydration(withEventReplay()),
    // Initialize metadata on app startup
    {
      provide: APP_INITIALIZER,
      useFactory: initializeAppFactory,
      deps: [MetadataService],
      multi: true
    }
  ]
};
