import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { IconService } from '../../shared/services/icon.service';
import { SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './about.component.html',
  styleUrl: './about.component.css'
})
export class AboutComponent {
  private iconService = inject(IconService);

  features = [
    {
      title: 'Context-Aware Analysis',
      description: 'GPT analyzes cards with full awareness of your investigator, campaign difficulty, and current game state.',
      icon: 'brain'
    },
    {
      title: 'Dynamic Axioms',
      description: 'Over 21 game mechanics axioms that adapt in real-time based on context (expert difficulty, Path to Carcosa horror focus, etc.).',
      icon: 'settings'
    },
    {
      title: 'Multi-Analysis Types',
      description: 'Card strength, synergy analysis, and optimal timing recommendations for any situation.',
      icon: 'target'
    },
    {
      title: 'Threat Assessment',
      description: 'Real-time danger level calculation based on doom pressure, enemy threats, and investigator health.',
      icon: 'analysis'
    },
    {
      title: 'Campaign Integration',
      description: 'Precomputed scenario data and encounter deck analysis for accurate threat modeling.',
      icon: 'campaign'
    },
    {
      title: 'Investigator Roles',
      description: 'Role-specific value adjustments (fighters prioritize damage, seekers value clues, etc.).',
      icon: 'investigator'
    }
  ];

  getIcon(iconName: string): SafeHtml {
    return this.iconService.getIcon(iconName);
  }

  techStack = [
    { name: 'Angular 18', description: 'Modern reactive frontend with signals' },
    { name: 'FastAPI', description: 'High-performance Python backend' },
    { name: 'PostgreSQL', description: 'Robust card database with full ArkhamDB integration' },
    { name: 'OpenAI GPT-4o', description: 'Advanced card analysis with context-aware prompts' },
    { name: 'Domain-Driven Design', description: 'Clean architecture with separation of concerns' },
    { name: 'Async Processing', description: 'Non-blocking analysis with rate limiting' }
  ];
}