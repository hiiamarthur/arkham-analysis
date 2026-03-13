import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection, provideAppInitializer, PLATFORM_ID, inject } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { lastValueFrom } from 'rxjs';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { MetadataService } from './services/metadata.service';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(withFetch()),
    provideClientHydration(withEventReplay()),
    provideAppInitializer(() => {
      const platformId = inject(PLATFORM_ID);
      if (isPlatformBrowser(platformId)) {
        const metadataService = inject(MetadataService);
        return lastValueFrom(metadataService.initializeMetadata());
      }
      return Promise.resolve();
    }),
  ]
};
