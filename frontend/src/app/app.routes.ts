import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./components/dashboard/dashboard.component').then(m => m.DashboardComponent),
    data: {
      title: 'Dashboard',
      description: 'Platform overview — investigator pool stats, scenario coverage, and meta insights from published decks.'
    }
  },
  {
    path: 'analysis',
    loadComponent: () => import('./components/card-analysis/card-analysis.component').then(m => m.CardAnalysisComponent),
    data: {
      title: 'Card Analysis',
      description: 'Browse cards, inspect deck performance, and run context-aware analysis.'
    }
  },
  {
    path: 'analysis/:code',
    loadComponent: () => import('./components/card-analysis/card-analysis.component').then(m => m.CardAnalysisComponent),
    data: {
      title: 'Card Analysis',
      description: 'Card details and deck statistics.'
    }
  },
  {
    path: 'threat-assessment',
    loadComponent: () => import('./components/threat-assessment/threat-assessment.component').then(m => m.ThreatAssessmentComponent),
    data: {
      title: 'Threat Assessment',
      description: 'Quickly estimate scenario danger level against your party and chaos bag context.'
    }
  },
  {
    path: 'investigators',
    loadComponent: () => import('./components/investigators/investigators.component').then(m => m.InvestigatorsComponent),
    data: {
      title: 'Investigators',
      description: 'Browse investigators and view competitive deck statistics, trends, and build recommendations.'
    }
  },
  {
    path: 'about',
    loadComponent: () => import('./components/about/about.component').then(m => m.AboutComponent),
    data: {
      title: 'About',
      description: 'What Arkham Analysis is, where the data comes from, and how to interpret the stats.'
    }
  },
  {
    path: '**',
    redirectTo: '/dashboard'
  }
];
