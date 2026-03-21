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
      description: 'Arkham Horror LCG analytics dashboard — live meta insights, top investigators, faction share, and card trends from thousands of published ArkhamDB decks.'
    }
  },
  {
    path: 'analysis',
    loadComponent: () => import('./components/card-analysis/card-analysis.component').then(m => m.CardAnalysisComponent),
    data: {
      title: 'Card Analysis',
      description: 'Browse every Arkham Horror LCG card — filter by faction, type, trait, and cost. View deck inclusion rates, usage trends, and investigator synergies.'
    }
  },
  {
    path: 'analysis/:code',
    loadComponent: () => import('./components/card-analysis/card-analysis.component').then(m => m.CardAnalysisComponent),
    data: {
      title: 'Card Analysis',
      description: 'Arkham Horror LCG card statistics — deck inclusion rate, usage trends, top investigators, and synergy data sourced from ArkhamDB.'
    }
  },
  {
    path: 'threat-assessment',
    loadComponent: () => import('./components/threat-assessment/threat-assessment.component').then(m => m.ThreatAssessmentComponent),
    data: {
      title: 'Threat Assessment',
      description: 'Arkham Horror LCG scenario threat calculator — assess chaos bag danger, scenario difficulty, and party composition for any campaign and investigator setup.'
    }
  },
  {
    path: 'investigators',
    loadComponent: () => import('./components/investigators/investigators.component').then(m => m.InvestigatorsComponent),
    data: {
      title: 'Investigators',
      description: 'All Arkham Horror LCG investigators — meta share, staple cards, deck archetypes, rising trends, and build recommendations from competitive ArkhamDB deck data.'
    }
  },
  {
    path: 'investigators/:code',
    loadComponent: () => import('./components/investigators/investigators.component').then(m => m.InvestigatorsComponent),
    data: {
      title: 'Investigators',
      description: 'All Arkham Horror LCG investigators — meta share, staple cards, deck archetypes, rising trends, and build recommendations from competitive ArkhamDB deck data.'
    }
  },
  {
    path: 'pool-playground',
    loadComponent: () => import('./components/pool-compare/pool-compare.component').then(m => m.PoolCompareComponent),
    data: {
      title: 'Pool Playground',
      description: 'Compare card pools between Arkham Horror LCG investigators — find shared cards, intersections, and exclusive picks to plan multi-investigator parties.'
    }
  },
  {
    path: 'about',
    loadComponent: () => import('./components/about/about.component').then(m => m.AboutComponent),
    data: {
      title: 'About',
      description: 'About Arkham Analysis — an open analytics platform for Arkham Horror: The Card Game, powered by ArkhamDB deck data. Learn how stats are calculated and how to use the tools.'
    }
  },
  {
    path: '**',
    redirectTo: '/dashboard'
  }
];
