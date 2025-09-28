import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./components/dashboard/dashboard.component').then(m => m.DashboardComponent)
  },
  {
    path: 'analysis',
    loadComponent: () => import('./components/card-analysis/card-analysis.component').then(m => m.CardAnalysisComponent)
  },
  {
    path: 'threat-assessment',
    loadComponent: () => import('./components/threat-assessment/threat-assessment.component').then(m => m.ThreatAssessmentComponent)
  },
  {
    path: 'about',
    loadComponent: () => import('./components/about/about.component').then(m => m.AboutComponent)
  },
  {
    path: '**',
    redirectTo: '/dashboard'
  }
];
