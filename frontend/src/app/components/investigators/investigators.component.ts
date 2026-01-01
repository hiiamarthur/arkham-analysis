import { Component, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DataTableComponent, TableColumn, TableConfig } from '../../shared/components/data-table.component';

interface Investigator {
  id: string;
  name: string;
  class: string;
  willpower: number;
  intellect: number;
  combat: number;
  agility: number;
  health: number;
  sanity: number;
  deckSize: number;
  expansion: string;
  popularity: number;
}

interface InvestigatorCard {
  code: string;
  name: string;
  type: string;
  cost: number;
  usageCount: number;
  winRate: number;
}

interface InvestigatorStats {
  totalGames: number;
  winRate: number;
  averageXP: number;
  favoriteCards: InvestigatorCard[];
  deckArchetypes: { name: string; percentage: number }[];
  scenarioPerformance: { scenario: string; winRate: number }[];
}

@Component({
  selector: 'app-investigators',
  standalone: true,
  imports: [CommonModule, DataTableComponent],
  templateUrl: './investigators.component.html',
  styleUrl: './investigators.component.css'
})
export class InvestigatorsComponent {
  // Expose Math to template
  Math = Math;
  
  // Selected investigator
  selectedInvestigator = signal<Investigator | null>(null);

  // All investigators data
  investigators = signal<Investigator[]>([
    {
      id: '01001',
      name: 'Roland Banks',
      class: 'Guardian',
      willpower: 3,
      intellect: 3,
      combat: 4,
      agility: 2,
      health: 9,
      sanity: 5,
      deckSize: 30,
      expansion: 'Core Set',
      popularity: 92
    },
    {
      id: '01002',
      name: 'Daisy Walker',
      class: 'Seeker',
      willpower: 3,
      intellect: 5,
      combat: 2,
      agility: 2,
      health: 5,
      sanity: 9,
      deckSize: 30,
      expansion: 'Core Set',
      popularity: 88
    },
    {
      id: '01003',
      name: '"Skids" O\'Toole',
      class: 'Rogue',
      willpower: 2,
      intellect: 3,
      combat: 3,
      agility: 4,
      health: 8,
      sanity: 6,
      deckSize: 30,
      expansion: 'Core Set',
      popularity: 75
    },
    {
      id: '01004',
      name: 'Agnes Baker',
      class: 'Mystic',
      willpower: 5,
      intellect: 2,
      combat: 2,
      agility: 3,
      health: 6,
      sanity: 8,
      deckSize: 30,
      expansion: 'Core Set',
      popularity: 85
    },
    {
      id: '01005',
      name: 'Wendy Adams',
      class: 'Survivor',
      willpower: 4,
      intellect: 3,
      combat: 1,
      agility: 4,
      health: 7,
      sanity: 7,
      deckSize: 30,
      expansion: 'Core Set',
      popularity: 80
    },
    {
      id: '02001',
      name: 'Zoey Samaras',
      class: 'Guardian',
      willpower: 4,
      intellect: 2,
      combat: 4,
      agility: 2,
      health: 9,
      sanity: 6,
      deckSize: 30,
      expansion: 'The Dunwich Legacy',
      popularity: 90
    },
    {
      id: '02002',
      name: 'Rex Murphy',
      class: 'Seeker',
      willpower: 3,
      intellect: 4,
      combat: 1,
      agility: 3,
      health: 6,
      sanity: 9,
      deckSize: 30,
      expansion: 'The Dunwich Legacy',
      popularity: 87
    },
    {
      id: '02003',
      name: 'Jenny Barnes',
      class: 'Rogue',
      willpower: 3,
      intellect: 3,
      combat: 3,
      agility: 3,
      health: 8,
      sanity: 7,
      deckSize: 30,
      expansion: 'The Dunwich Legacy',
      popularity: 82
    },
    {
      id: '02004',
      name: 'Jim Culver',
      class: 'Mystic',
      willpower: 4,
      intellect: 3,
      combat: 3,
      agility: 2,
      health: 7,
      sanity: 8,
      deckSize: 30,
      expansion: 'The Dunwich Legacy',
      popularity: 78
    },
    {
      id: '02005',
      name: '"Ashcan" Pete',
      class: 'Survivor',
      willpower: 4,
      intellect: 2,
      combat: 2,
      agility: 3,
      health: 6,
      sanity: 5,
      deckSize: 30,
      expansion: 'The Dunwich Legacy',
      popularity: 83
    }
  ]);

  // Investigator stats (mock data for selected investigator)
  investigatorStats = computed<InvestigatorStats | null>(() => {
    const selected = this.selectedInvestigator();
    if (!selected) return null;

    // Generate mock stats based on investigator
    return {
      totalGames: Math.floor(Math.random() * 100) + 50,
      winRate: Math.floor(Math.random() * 40) + 50,
      averageXP: Math.floor(Math.random() * 20) + 10,
      favoriteCards: this.getFavoriteCardsForInvestigator(selected),
      deckArchetypes: this.getDeckArchetypesForInvestigator(selected),
      scenarioPerformance: this.getScenarioPerformanceForInvestigator(selected)
    };
  });

  // Table columns for investigators list
  investigatorColumns: TableColumn[] = [
    { key: 'name', label: 'Name', sortable: true, searchable: true, width: '200px' },
    { key: 'class', label: 'Class', sortable: true, filterable: true, width: '120px' },
    { key: 'willpower', label: 'Willpower', sortable: true, type: 'number', width: '100px' },
    { key: 'intellect', label: 'Intellect', sortable: true, type: 'number', width: '100px' },
    { key: 'combat', label: 'Combat', sortable: true, type: 'number', width: '100px' },
    { key: 'agility', label: 'Agility', sortable: true, type: 'number', width: '100px' },
    { key: 'health', label: 'Health', sortable: true, type: 'number', width: '80px' },
    { key: 'sanity', label: 'Sanity', sortable: true, type: 'number', width: '80px' },
    { key: 'expansion', label: 'Expansion', sortable: true, filterable: true },
    { key: 'popularity', label: 'Popularity', sortable: true, type: 'number', width: '100px', render: (value: number) => `${value}%` }
  ];

  // Table columns for favorite cards
  cardColumns: TableColumn[] = [
    { key: 'name', label: 'Card Name', sortable: true, searchable: true },
    { key: 'type', label: 'Type', sortable: true, filterable: true, width: '120px' },
    { key: 'cost', label: 'Cost', sortable: true, type: 'number', width: '80px' },
    { key: 'usageCount', label: 'Times Used', sortable: true, type: 'number', width: '120px' },
    { key: 'winRate', label: 'Win Rate', sortable: true, type: 'number', width: '100px', render: (value: number) => `${value}%` }
  ];

  // Table config
  tableConfig: TableConfig = {
    pageSize: 10,
    pageSizeOptions: [5, 10, 25, 50],
    showPagination: true,
    showSearch: true,
    showColumnToggle: true,
    showFilters: true,
    striped: true,
    hoverable: true,
    bordered: true,
    responsive: true
  };

  cardTableConfig: TableConfig = {
    pageSize: 10,
    pageSizeOptions: [10, 25, 50],
    showPagination: true,
    showSearch: true,
    showColumnToggle: false,
    showFilters: false,
    striped: true,
    hoverable: true,
    bordered: true,
    responsive: true
  };

  // Event handlers
  onInvestigatorClick(investigator: Investigator) {
    this.selectedInvestigator.set(investigator);
    // Scroll to details section
    setTimeout(() => {
      document.getElementById('investigator-details')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  }

  backToList() {
    this.selectedInvestigator.set(null);
  }

  // Helper methods to generate mock data
  private getFavoriteCardsForInvestigator(investigator: Investigator): InvestigatorCard[] {
    const cardsByClass: Record<string, InvestigatorCard[]> = {
      'Guardian': [
        { code: '01020', name: 'Machete', type: 'Asset', cost: 3, usageCount: 45, winRate: 72 },
        { code: '01030', name: 'Emergency Cache', type: 'Asset', cost: 0, usageCount: 52, winRate: 65 },
        { code: '01076', name: 'Beat Cop', type: 'Asset', cost: 4, usageCount: 38, winRate: 68 },
        { code: '01088', name: 'Guard Dog', type: 'Asset', cost: 3, usageCount: 33, winRate: 64 },
        { code: '01017', name: 'Physical Training', type: 'Asset', cost: 2, usageCount: 41, winRate: 70 }
      ],
      'Seeker': [
        { code: '01022', name: 'Magnifying Glass', type: 'Asset', cost: 1, usageCount: 58, winRate: 75 },
        { code: '01039', name: 'Working a Hunch', type: 'Event', cost: 2, usageCount: 43, winRate: 71 },
        { code: '01024', name: 'Dr. Milan Christopher', type: 'Asset', cost: 4, usageCount: 40, winRate: 78 },
        { code: '01040', name: 'Barricade', type: 'Event', cost: 0, usageCount: 35, winRate: 66 },
        { code: '01025', name: 'Hyperawareness', type: 'Asset', cost: 2, usageCount: 38, winRate: 69 }
      ],
      'Rogue': [
        { code: '01027', name: 'Lockpicks', type: 'Asset', cost: 3, usageCount: 47, winRate: 73 },
        { code: '01030', name: 'Emergency Cache', type: 'Asset', cost: 0, usageCount: 55, winRate: 68 },
        { code: '01047', name: 'Elusive', type: 'Event', cost: 2, usageCount: 42, winRate: 70 },
        { code: '01028', name: 'Burglary', type: 'Skill', cost: 0, usageCount: 39, winRate: 67 },
        { code: '01048', name: 'Backstab', type: 'Event', cost: 3, usageCount: 36, winRate: 72 }
      ],
      'Mystic': [
        { code: '01032', name: 'Shrivelling', type: 'Asset', cost: 3, usageCount: 50, winRate: 76 },
        { code: '01053', name: 'Ward of Protection', type: 'Event', cost: 1, usageCount: 48, winRate: 74 },
        { code: '01031', name: 'Forbidden Knowledge', type: 'Asset', cost: 0, usageCount: 44, winRate: 69 },
        { code: '01033', name: 'Scrying', type: 'Asset', cost: 1, usageCount: 37, winRate: 68 },
        { code: '01034', name: 'Arcane Studies', type: 'Asset', cost: 2, usageCount: 41, winRate: 71 }
      ],
      'Survivor': [
        { code: '01036', name: 'Baseball Bat', type: 'Asset', cost: 2, usageCount: 46, winRate: 70 },
        { code: '01060', name: 'Lucky!', type: 'Event', cost: 1, usageCount: 53, winRate: 77 },
        { code: '01061', name: 'Survival Instinct', type: 'Skill', cost: 0, usageCount: 40, winRate: 65 },
        { code: '01037', name: 'Rabbit\'s Foot', type: 'Asset', cost: 1, usageCount: 42, winRate: 72 },
        { code: '01080', name: 'Leather Coat', type: 'Asset', cost: 0, usageCount: 38, winRate: 68 }
      ]
    };

    return cardsByClass[investigator.class] || [];
  }

  private getDeckArchetypesForInvestigator(investigator: Investigator): { name: string; percentage: number }[] {
    const archetypesByClass: Record<string, { name: string; percentage: number }[]> = {
      'Guardian': [
        { name: 'Monster Hunter', percentage: 45 },
        { name: 'Tank/Protector', percentage: 30 },
        { name: 'Hybrid Fighter-Cluer', percentage: 25 }
      ],
      'Seeker': [
        { name: 'Clue Vacuum', percentage: 50 },
        { name: 'Big Hand Combo', percentage: 35 },
        { name: 'Support/Tutor', percentage: 15 }
      ],
      'Rogue': [
        { name: 'Money Engine', percentage: 40 },
        { name: 'Evade Master', percentage: 35 },
        { name: 'Damage Dealer', percentage: 25 }
      ],
      'Mystic': [
        { name: 'Spell Slinger', percentage: 45 },
        { name: 'Curse Manipulator', percentage: 30 },
        { name: 'Mystic Cluer', percentage: 25 }
      ],
      'Survivor': [
        { name: 'Recursion Engine', percentage: 40 },
        { name: 'Will to Survive', percentage: 35 },
        { name: 'Exile Build', percentage: 25 }
      ]
    };

    return archetypesByClass[investigator.class] || [];
  }

  private getScenarioPerformanceForInvestigator(investigator: Investigator): { scenario: string; winRate: number }[] {
    return [
      { scenario: 'The Gathering', winRate: Math.floor(Math.random() * 30) + 60 },
      { scenario: 'The Midnight Masks', winRate: Math.floor(Math.random() * 30) + 55 },
      { scenario: 'The Devourer Below', winRate: Math.floor(Math.random() * 30) + 50 },
      { scenario: 'Extracurricular Activity', winRate: Math.floor(Math.random() * 30) + 55 },
      { scenario: 'The House Always Wins', winRate: Math.floor(Math.random() * 30) + 52 }
    ];
  }

  getClassColor(className: string): string {
    const colors: Record<string, string> = {
      'Guardian': '#2b80c5',
      'Seeker': '#ec8b26',
      'Rogue': '#107116',
      'Mystic': '#4e1a45',
      'Survivor': '#cc3038',
      'Neutral': '#5a5a5a'
    };
    return colors[className] || '#5a5a5a';
  }
}
