import { Component, OnInit, signal, inject, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { CardModalService } from '../../services/card-modal.service';
import { CardModalComponent } from '../../shared/components/card-modal.component';
import { IconService } from '../../shared/services/icon.service';
import { SafeHtml } from '@angular/platform-browser';

export interface Investigator {
  code: string;
  name: string;
  faction_code: string;
}

export interface PoolCard {
  code: string;
  name: string;
  faction_code: string;
  type_code: string;
  xp: number | null;
  imagesrc: string | null;
}

export interface ArchetypePoolCard {
  code: string;
  name: string;
  xp: number;
  cost: number | null;
  faction_code: string;
  type_code: string | null;
  imagesrc: string | null;
  archetypes: string[] | null;
  archetype_reason: string | null;
  is_unique: boolean | null;
  has_upgrade: boolean;
}

export interface ArchetypeTier {
  xp: number;
  cards: ArchetypePoolCard[];
}

export interface ArchetypePoolResponse {
  archetype: string;
  investigator_code: string;
  investigator_name: string | null;
  card_type: string | null;
  tiers: ArchetypeTier[];
  total: number;
}

export interface UpgradeNode {
  code: string;
  name: string;
  xp: number;
  cost: number | null;
  faction_code: string;
  type_code: string | null;
  type_name: string | null;
  imagesrc: string | null;
  archetypes: string[] | null;
  archetype_reason: string | null;
  traits: string[];
  skill_willpower: number | null;
  skill_intellect: number | null;
  skill_combat: number | null;
  skill_agility: number | null;
  skill_wild: number | null;
  text: string | null;
  pack_name: string | null;
  is_unique: boolean | null;
  exceptional: boolean | null;
}

export interface UpgradeChain {
  chain_key: string;
  name: string;
  faction_code: string;
  type_code: string | null;
  archetypes: string[] | null;
  nodes: UpgradeNode[];
}

const TYPE_LABELS: Record<string, string> = {
  asset: 'Asset',
  event: 'Event',
  skill: 'Skill',
};

const ARCHETYPE_COLORS: Record<string, string> = {
  combat: '#e05252',
  clue: '#4db8d4',
  protection: '#6dbe89',
  economy: '#f0c040',
  draw: '#a07acc',
  tech: '#e8904a',
};

const ARCHETYPE_LABELS: Record<string, string> = {
  combat: 'Combat',
  clue: 'Clue',
  protection: 'Protect',
  economy: 'Economy',
  draw: 'Draw',
  tech: 'Tech',
};

const FACTION_COLORS: Record<string, string> = {
  guardian: '#4299e1',
  seeker: '#f6ad55',
  rogue: '#48bb78',
  mystic: '#9f7aea',
  survivor: '#fc814a',
  neutral: '#a0aec0',
};

@Component({
  selector: 'app-upgrade-builder',
  standalone: true,
  imports: [CommonModule, FormsModule, CardModalComponent],
  templateUrl: './upgrade-builder.component.html',
  styleUrls: ['./upgrade-builder.component.css'],
})
export class UpgradeBuilderComponent implements OnInit {
  private http = inject(HttpClient);
  cardModalService = inject(CardModalService);
  private iconService = inject(IconService);

  // Investigators list
  investigators = signal<Investigator[]>([]);

  // Selected investigator
  selectedInvestigator = signal<Investigator | null>(null);
  investigatorSearch = signal('');
  showInvestigatorDropdown = signal(false);

  // Base card search within investigator pool
  poolCards = signal<PoolCard[]>([]);
  selectedCard = signal<PoolCard | null>(null);
  cardSearch = signal('');
  showCardDropdown = signal(false);

  // Filters
  selectedType = signal('');
  selectedArchetype = signal('');
  selectedSlot = signal('');

  // Legacy signals kept to avoid template errors — chains section removed
  chains = signal<UpgradeChain[]>([]);
  loading = signal(false);
  loadingPool = signal(false);
  total = signal(0);
  investigatorName = signal('');

  // Results — archetype pool (XP tier view)
  archetypePool = signal<ArchetypeTier[]>([]);
  archetypePoolTotal = signal(0);
  loadingArchetypePool = signal(false);

  types = Object.entries(TYPE_LABELS).map(([k, v]) => ({ code: k, label: v }));
  archetypes = Object.entries(ARCHETYPE_LABELS).map(([k, v]) => ({ code: k, label: v }));
  slots = [
    { code: 'Hand', label: 'Hand' },
    { code: 'Hand x2', label: 'Hand ×2' },
    { code: 'Arcane', label: 'Arcane' },
    { code: 'Accessory', label: 'Accessory' },
    { code: 'Ally', label: 'Ally' },
    { code: 'Body', label: 'Body' },
    { code: 'Tarot', label: 'Tarot' },
  ];
  archetypeColors = ARCHETYPE_COLORS;
  archetypeLabels = ARCHETYPE_LABELS;
  factionColors = FACTION_COLORS;

  filteredInvestigators = computed(() => {
    const q = this.investigatorSearch().toLowerCase();
    if (!q) return this.investigators().slice(0, 12);
    return this.investigators()
      .filter(i => i.name.toLowerCase().includes(q))
      .slice(0, 12);
  });

  filteredPoolCards = computed(() => {
    const q = this.cardSearch().toLowerCase();
    const pool = this.poolCards();
    if (!q) return pool.slice(0, 10);
    return pool.filter(c => c.name.toLowerCase().includes(q)).slice(0, 10);
  });

  ngOnInit(): void {
    this.loadInvestigators();
  }

  loadInvestigators(): void {
    this.http
      .get<Investigator[]>(`${environment.apiUrl}/cards/metadata/investigators`)
      .subscribe(list => this.investigators.set(list));
  }

  selectInvestigator(inv: Investigator): void {
    this.selectedInvestigator.set(inv);
    this.investigatorSearch.set(inv.name);
    this.showInvestigatorDropdown.set(false);
    this.selectedCard.set(null);
    this.cardSearch.set('');
    this.loadPoolCards(inv.code);
    this.loadArchetypePool();
  }

  clearInvestigator(): void {
    this.selectedInvestigator.set(null);
    this.investigatorSearch.set('');
    this.selectedCard.set(null);
    this.cardSearch.set('');
    this.poolCards.set([]);
    this.chains.set([]);
    this.total.set(0);
    this.archetypePool.set([]);
    this.archetypePoolTotal.set(0);
    this.selectedSlot.set('');
  }

  loadPoolCards(invCode: string): void {
    this.loadingPool.set(true);
    this.http
      .get<{ cards: PoolCard[] }>(`${environment.apiUrl}/cards/investigator/${invCode}/card-pool`)
      .subscribe({
        next: res => {
          // Only keep cards with xp data (part of an upgrade chain)
          const withXp = (res.cards || []).filter(c => c.xp !== null && c.xp !== undefined);
          this.poolCards.set(withXp);
          this.loadingPool.set(false);
        },
        error: () => this.loadingPool.set(false),
      });
  }

  selectCard(card: PoolCard): void {
    this.selectedCard.set(card);
    this.cardSearch.set(card.name);
    this.showCardDropdown.set(false);
  }

  clearCard(): void {
    this.selectedCard.set(null);
    this.cardSearch.set('');
  }

  loadChains(): void {
    const inv = this.selectedInvestigator();
    if (!inv) return;

    this.loading.set(true);
    let params = new HttpParams();
    const type = this.selectedType();
    const archetype = this.selectedArchetype();
    const slot = this.selectedSlot();
    const card = this.selectedCard();

    if (type) params = params.set('card_type', type);
    if (archetype) params = params.set('archetype', archetype);
    if (slot) params = params.set('slot', slot);
    if (card) params = params.set('card_code', card.code);

    this.http
      .get<{ chains: UpgradeChain[]; total: number; investigator_name: string }>(
        `${environment.apiUrl}/cards/investigator/${inv.code}/upgrade-chains`,
        { params }
      )
      .subscribe({
        next: res => {
          this.chains.set(res.chains);
          this.total.set(res.total);
          this.investigatorName.set(res.investigator_name || inv.name);
          this.loading.set(false);
        },
        error: () => this.loading.set(false),
      });
  }

  setSlot(s: string): void {
    this.selectedSlot.set(this.selectedSlot() === s ? '' : s);
    this.loadArchetypePool();
  }

  setType(t: string): void {
    const next = this.selectedType() === t ? '' : t;
    this.selectedType.set(next);
    if (next !== 'asset') this.selectedSlot.set('');
    this.loadArchetypePool();
  }

  setArchetype(a: string): void {
    this.selectedArchetype.set(this.selectedArchetype() === a ? '' : a);
    this.loadArchetypePool();
  }

  loadArchetypePool(): void {
    const inv = this.selectedInvestigator();
    if (!inv) return;

    this.loadingArchetypePool.set(true);
    let params = new HttpParams();
    const archetype = this.selectedArchetype();
    const type = this.selectedType();
    const slot = this.selectedSlot();
    if (archetype) params = params.set('archetype', archetype);
    if (type) params = params.set('card_type', type);
    if (slot) params = params.set('slot', slot);

    this.http
      .get<ArchetypePoolResponse>(
        `${environment.apiUrl}/cards/investigator/${inv.code}/archetype-pool`,
        { params }
      )
      .subscribe({
        next: res => {
          this.archetypePool.set(res.tiers);
          this.archetypePoolTotal.set(res.total);
          this.loadingArchetypePool.set(false);
        },
        error: () => this.loadingArchetypePool.set(false),
      });
  }

  poolCardArchetypeLabel(card: ArchetypePoolCard): string {
    return (card.archetypes || []).map(a => ARCHETYPE_LABELS[a] || a).join(' · ');
  }

  openCard(code: string): void {
    this.cardModalService.openCardModal(code);
  }

  getIcon(name: string): SafeHtml {
    return this.iconService.getIcon(name);
  }

  getFactionColor(code: string): string {
    return FACTION_COLORS[code] || '#a0aec0';
  }

  getXpBadgeClass(xp: number): string {
    if (xp === 0) return 'xp-badge xp-0';
    if (xp <= 2) return 'xp-badge xp-low';
    if (xp <= 4) return 'xp-badge xp-mid';
    return 'xp-badge xp-high';
  }

  xpDelta(chain: UpgradeChain, idx: number): number {
    if (idx === 0) return 0;
    return chain.nodes[idx].xp - chain.nodes[idx - 1].xp;
  }

  isSelectedCardInChain(chain: UpgradeChain): boolean {
    const c = this.selectedCard();
    if (!c) return false;
    return chain.nodes.some(n => n.code === c.code || n.name === c.name);
  }

  trackChain(_: number, chain: UpgradeChain): string { return chain.chain_key; }
  trackNode(_: number, node: UpgradeNode): string { return node.code; }
  trackInv(_: number, inv: Investigator): string { return inv.code; }
  trackCard(_: number, card: PoolCard): string { return card.code; }
  trackTier(_: number, tier: ArchetypeTier): number { return tier.xp; }
  trackPoolCard(_: number, card: ArchetypePoolCard): string { return card.code; }
}
