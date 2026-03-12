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
      title: 'Investigator Chronicles',
      description: 'Track deck trends, staple cards, rising picks, and archetype patterns across thousands of published investigator decks. Know what the community reaches for.',
      icon: 'investigator'
    },
    {
      title: 'Chaos Bag Probability',
      description: 'Exact pass probability calculations for every investigator stat against any scenario\'s chaos bag — accounting for skull chains, bless/curse cascades, and frost mechanics.',
      icon: 'skull'
    },
    {
      title: 'Party vs Scenario',
      description: 'Select your investigators and see how each stat line performs against the actual bag. Ranked by scenario demand — who is best suited for this particular darkness.',
      icon: 'combat'
    },
    {
      title: 'Scenario Threat Assessment',
      description: 'Read the scenario before it reads you. Enemy density, shroud distribution, treachery test demands, doom pressure — all distilled into a living threat level.',
      icon: 'analysis'
    },
    {
      title: 'Encounter Deck Intelligence',
      description: 'Understand what lurks in the encounter deck before it strikes. Card composition, victory points, special mechanics, and trait distribution per scenario.',
      icon: 'auto_fail'
    },
    {
      title: 'Campaign Context',
      description: 'Every campaign has its own chaos bag, its own test demands, its own rhythm. Analysis adapts to the full breadth of Arkham Horror\'s released content.',
      icon: 'campaign'
    }
  ];

  getIcon(iconName: string): SafeHtml {
    return this.iconService.getIcon(iconName);
  }
}
