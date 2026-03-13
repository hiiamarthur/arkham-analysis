import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection, APP_INITIALIZER, PLATFORM_ID } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { MetadataService } from './services/metadata.service';

/**
 * Initialize app metadata on app startup.
 * Skip during SSR/build to avoid hitting unavailable backend.
 */
function initializeAppFactory(metadataService: MetadataService, platformId: object) {
  return () => {
    if (isPlatformBrowser(platformId)) {
      return metadataService.initializeMetadata().toPromise();
    }
    return Promise.resolve();
  };
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(withFetch()),
    provideClientHydration(withEventReplay()),
    {
      provide: APP_INITIALIZER,
      useFactory: initializeAppFactory,
      deps: [MetadataService, PLATFORM_ID],
      multi: true
    }
  ]
};
