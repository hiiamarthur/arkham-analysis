import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './about.component.html',
  styleUrl: './about.component.css'
})
export class AboutComponent {
  features = [
    {
      title: 'Context-Aware Analysis',
      description: 'GPT analyzes cards with full awareness of your investigator, campaign difficulty, and current game state.',
      icon: '🧠'
    },
    {
      title: 'Dynamic Axioms',
      description: 'Over 21 game mechanics axioms that adapt in real-time based on context (expert difficulty, Path to Carcosa horror focus, etc.).',
      icon: '⚙️'
    },
    {
      title: 'Multi-Analysis Types',
      description: 'Card strength, synergy analysis, and optimal timing recommendations for any situation.',
      icon: '🎯'
    },
    {
      title: 'Threat Assessment',
      description: 'Real-time danger level calculation based on doom pressure, enemy threats, and investigator health.',
      icon: '📊'
    },
    {
      title: 'Campaign Integration',
      description: 'Precomputed scenario data and encounter deck analysis for accurate threat modeling.',
      icon: '🗂️'
    },
    {
      title: 'Investigator Roles',
      description: 'Role-specific value adjustments (fighters prioritize damage, seekers value clues, etc.).',
      icon: '👥'
    }
  ];

  techStack = [
    { name: 'Angular 18', description: 'Modern reactive frontend with signals' },
    { name: 'FastAPI', description: 'High-performance Python backend' },
    { name: 'PostgreSQL', description: 'Robust card database with full ArkhamDB integration' },
    { name: 'OpenAI GPT-4o', description: 'Advanced card analysis with context-aware prompts' },
    { name: 'Domain-Driven Design', description: 'Clean architecture with separation of concerns' },
    { name: 'Async Processing', description: 'Non-blocking analysis with rate limiting' }
  ];
}