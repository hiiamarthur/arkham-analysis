import { Component, signal, computed, inject, OnInit, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { SafeHtml, DomSanitizer } from '@angular/platform-browser';
import { InvestigatorService, CardPoolEntry, InvestigatorMetadata } from '../../services/investigator.service';
import { ArkhamSvgIconsService } from '../../shared/services/arkham-svg-icons.service';

type InvMode = 'any' | 'in' | 'out';

interface PoolSlot {
  code: string;
  name: string;
  faction_code: string;
  pool: CardPoolEntry[];
  loading: boolean;
}

interface ComparedCard extends CardPoolEntry {
  presentIn: boolean[];
  shareCount: number;
}

interface CardGroup {
  label: string;
  cards: ComparedCard[];
  shareCount: number;
  color: string;
}

@Component({
  selector: 'app-pool-compare',
  standalone: true,
  imports: [CommonModule, FormsModule],
  // RouterModule not needed — we use Router.navigate directly
  templateUrl: './pool-compare.component.html',
  styleUrl: './pool-compare.component.css',
})
export class PoolCompareComponent implements OnInit {
  private investigatorService = inject(InvestigatorService);
  private arkhamIconsService = inject(ArkhamSvgIconsService);
  private sanitizer = inject(DomSanitizer);
  private router = inject(Router);

  goToCard(code: string): void {
    this.router.navigate(['/analysis', code]);
  }

  allInvestigators = signal<InvestigatorMetadata[]>([]);
  slots = signal<(PoolSlot | null)[]>([null, null, null, null]);

  // Investigator set-operation modes (indexed by slot position 0-3)
  invModes = signal<InvMode[]>(['any', 'any', 'any', 'any']);

  slotSearch: string[] = ['', '', '', ''];
  slotOpen: boolean[] = [false, false, false, false];

  xpFilter      = signal<'all' | '0' | '1+'>('all');
  typeFilter    = signal<Set<string>>(new Set());
  factionFilter = signal<Set<string>>(new Set());
  slotFilter    = signal<Set<string>>(new Set());
  traitFilter   = signal<Set<string>>(new Set());
  packFilter    = signal<Set<string>>(new Set());
  costFilter    = signal<Set<string>>(new Set());
  nameSearch    = signal('');
  textSearch    = signal('');

  guideOpen = false;
  showHelp = signal<boolean>(false);
  toggleHelp() { this.showHelp.update(v => !v); }

  // Dropdown open state for multi-select panels
  typeOpen    = false;
  factionOpen = false;
  slotOpen2   = false;
  traitOpen   = false;
  packOpen    = false;
  costOpen    = false;
  traitSearchTerm = '';

  readonly FACTION_COLORS: Record<string, string> = {
    guardian: '#2b80c5',
    seeker:   '#ec8b26',
    rogue:    '#107116',
    mystic:   '#4e1a45',
    survivor: '#cc3038',
    neutral:  '#6b7280',
  };

  readonly FACTION_LABELS: Record<string, string> = {
    guardian: 'Guardian', seeker: 'Seeker', rogue: 'Rogue',
    mystic: 'Mystic', survivor: 'Survivor', neutral: 'Neutral',
  };

  readonly TYPE_LABELS: Record<string, string> = {
    asset: 'Asset', event: 'Event', skill: 'Skill',
  };

  // ── Derived state ──────────────────────────────────────────────────────────

  activeSlots = computed(() => this.slots().filter((s): s is PoolSlot => s !== null));

  /** Slot-array indices (0-3) for each active investigator, in order */
  activeSlotIndices = computed(() =>
    this.slots().map((s, i) => s !== null ? i : -1).filter(i => i >= 0)
  );

  isLoading = computed(() => this.slots().some(s => s?.loading));

  comparedCards = computed<ComparedCard[]>(() => {
    const active = this.activeSlots();
    if (active.length < 2) return [];

    const map = new Map<string, ComparedCard>();
    active.forEach((inv, idx) => {
      inv.pool.forEach(card => {
        if (!map.has(card.code)) {
          map.set(card.code, {
            ...card,
            presentIn: new Array(active.length).fill(false),
            shareCount: 0,
          });
        }
        map.get(card.code)!.presentIn[idx] = true;
      });
    });
    map.forEach(c => { c.shareCount = c.presentIn.filter(Boolean).length; });

    return Array.from(map.values()).sort(
      (a, b) => b.shareCount - a.shareCount || a.name.localeCompare(b.name)
    );
  });

  filteredCards = computed<ComparedCard[]>(() => {
    const modes  = this.invModes();
    const indices = this.activeSlotIndices();
    let cards = this.comparedCards();

    // Investigator set-operation filter
    if (indices.some(i => modes[i] !== 'any')) {
      cards = cards.filter(card => {
        for (let k = 0; k < indices.length; k++) {
          const mode = modes[indices[k]];
          if (mode === 'in'  && !card.presentIn[k]) return false;
          if (mode === 'out' &&  card.presentIn[k]) return false;
        }
        return true;
      });
    }

    const name = this.nameSearch().trim().toLowerCase();
    if (name) cards = cards.filter(c => c.name.toLowerCase().includes(name));

    const text = this.textSearch().trim().toLowerCase();
    if (text) cards = cards.filter(c =>
      (c.text ?? '').toLowerCase().includes(text) ||
      (c.flavor ?? '').toLowerCase().includes(text)
    );

    const xp = this.xpFilter();
    if (xp === '0')  cards = cards.filter(c => c.xp === 0);
    if (xp === '1+') cards = cards.filter(c => c.xp >= 1);

    const types = this.typeFilter();
    if (types.size) cards = cards.filter(c => types.has(c.type_code));

    const factions = this.factionFilter();
    if (factions.size) cards = cards.filter(c =>
      factions.has(c.faction_code) ||
      (c.faction2_code != null && factions.has(c.faction2_code)) ||
      (c.faction3_code != null && factions.has(c.faction3_code))
    );

    const slots = this.slotFilter();
    if (slots.size) cards = cards.filter(c =>
      this.splitSlots(c.real_slot).some(s => slots.has(s))
    );

    const traits = this.traitFilter();
    if (traits.size) cards = cards.filter(c => c.traits.some(t => traits.has(t)));

    const packs = this.packFilter();
    if (packs.size) cards = cards.filter(c => c.pack_name != null && packs.has(c.pack_name));

    const costs = this.costFilter();
    if (costs.size) cards = cards.filter(c => {
      const key = c.cost == null ? 'X' : String(c.cost);
      return costs.has(key);
    });

    return cards;
  });

  groupedCards = computed<CardGroup[]>(() => {
    const active = this.activeSlots();
    const n = active.length;
    const cards = this.filteredCards();
    const groups: CardGroup[] = [];

    const fullShare = cards.filter(c => c.shareCount === n);
    if (fullShare.length) {
      groups.push({ label: `Shared by all ${n}`, cards: fullShare, shareCount: n, color: '#4ade80' });
    }
    for (let k = n - 1; k >= 2; k--) {
      const partial = cards.filter(c => c.shareCount === k);
      if (partial.length) {
        groups.push({ label: `Shared by ${k} of ${n}`, cards: partial, shareCount: k, color: '#facc15' });
      }
    }
    active.forEach((inv, idx) => {
      const excl = cards.filter(c => c.shareCount === 1 && c.presentIn[idx]);
      if (excl.length) {
        groups.push({
          label: `Only ${inv.name}`,
          cards: excl,
          shareCount: 1,
          color: this.FACTION_COLORS[inv.faction_code] ?? '#6b7280',
        });
      }
    });
    return groups;
  });

  unionSize = computed(() => this.comparedCards().length);
  intersectionSize = computed(() => {
    const n = this.activeSlots().length;
    return this.comparedCards().filter(c => c.shareCount === n).length;
  });

  availableFactions = computed(() => {
    const s = new Set<string>();
    this.comparedCards().forEach(c => {
      if (c.faction_code) s.add(c.faction_code);
      if (c.faction2_code) s.add(c.faction2_code!);
      if (c.faction3_code) s.add(c.faction3_code!);
    });
    return Array.from(s).sort();
  });

  availableTypes = computed(() =>
    Array.from(new Set(this.comparedCards().map(c => c.type_code))).sort()
  );

  availableSlots = computed(() => {
    const s = new Set<string>();
    this.comparedCards().forEach(c => this.splitSlots(c.real_slot).forEach(sl => s.add(sl)));
    return Array.from(s).sort();
  });

  availableTraits = computed(() =>
    Array.from(new Set(this.comparedCards().flatMap(c => c.traits))).sort()
  );

  availablePacks = computed(() =>
    Array.from(new Set(this.comparedCards().map(c => c.pack_name).filter((p): p is string => !!p))).sort()
  );

  availableCosts = computed(() => {
    const s = new Set<string>();
    this.comparedCards().forEach(c => s.add(c.cost == null ? 'X' : String(c.cost)));
    return Array.from(s).sort((a, b) => {
      if (a === 'X') return 1;
      if (b === 'X') return -1;
      return Number(a) - Number(b);
    });
  });

  filteredTraits = computed(() => {
    const q = this.traitSearchTerm.toLowerCase();
    return this.availableTraits().filter(t => !q || t.toLowerCase().includes(q));
  });

  readonly PAGE_SIZE = 30;

  collapsedGroups = signal<Set<string>>(new Set());
  groupPages = signal<Map<string, number>>(new Map());

  isGroupCollapsed(label: string): boolean {
    return this.collapsedGroups().has(label);
  }

  toggleGroup(label: string) {
    this.collapsedGroups.update(s => {
      const next = new Set(s);
      next.has(label) ? next.delete(label) : next.add(label);
      return next;
    });
  }

  getGroupPage(label: string): number {
    return this.groupPages().get(label) ?? 1;
  }

  private setGroupPage(label: string, page: number) {
    this.groupPages.update(m => {
      const next = new Map(m);
      next.set(label, page);
      return next;
    });
  }

  getPageCount(group: CardGroup): number {
    return Math.max(1, Math.ceil(group.cards.length / this.PAGE_SIZE));
  }

  getPagedCards(group: CardGroup): ComparedCard[] {
    const page = Math.min(this.getGroupPage(group.label), this.getPageCount(group));
    const start = (page - 1) * this.PAGE_SIZE;
    return group.cards.slice(start, start + this.PAGE_SIZE);
  }

  getPageStart(group: CardGroup): number {
    const page = Math.min(this.getGroupPage(group.label), this.getPageCount(group));
    return (page - 1) * this.PAGE_SIZE + 1;
  }

  getPageEnd(group: CardGroup): number {
    const page = Math.min(this.getGroupPage(group.label), this.getPageCount(group));
    return Math.min(page * this.PAGE_SIZE, group.cards.length);
  }

  prevPage(label: string) {
    const current = this.getGroupPage(label);
    if (current > 1) this.setGroupPage(label, current - 1);
  }

  nextPage(group: CardGroup) {
    const current = this.getGroupPage(group.label);
    if (current < this.getPageCount(group)) this.setGroupPage(group.label, current + 1);
  }

  goToPage(label: string, page: number, maxPage: number) {
    const clamped = Math.max(1, Math.min(page, maxPage));
    this.setGroupPage(label, clamped);
  }

  hasActiveInvFilter = computed(() =>
    this.activeSlotIndices().some(i => this.invModes()[i] !== 'any')
  );

  hasActiveFilters = computed(() =>
    !!this.nameSearch() || !!this.textSearch() ||
    !!this.typeFilter().size || !!this.factionFilter().size ||
    !!this.slotFilter().size || !!this.traitFilter().size ||
    !!this.packFilter().size || !!this.costFilter().size ||
    this.xpFilter() !== 'all' || this.hasActiveInvFilter()
  );

  // ── Lifecycle ──────────────────────────────────────────────────────────────

  ngOnInit() {
    this.investigatorService.getAllInvestigators().subscribe({
      next: list => this.allInvestigators.set(list),
    });
  }

  // ── Slot management ────────────────────────────────────────────────────────

  slotColor(idx: number): string {
    const s = this.slots()[idx];
    return s ? (this.FACTION_COLORS[s.faction_code] ?? '#6b7280') : '#3a3a4a';
  }

  openSearch(idx: number, event: MouseEvent) {
    event.stopPropagation();
    this.slotOpen = this.slotOpen.map((_, i) => i === idx) as boolean[];
    this.slotSearch[idx] = '';
  }

  closeSearch(idx: number) {
    setTimeout(() => { this.slotOpen[idx] = false; }, 160);
  }

  searchResults(idx: number): InvestigatorMetadata[] {
    const q = this.slotSearch[idx].toLowerCase();
    const taken = new Set(this.slots().filter(Boolean).map(s => s!.code));
    return this.allInvestigators()
      .filter(i => !taken.has(i.code) && (!q || i.name.toLowerCase().includes(q)))
      .slice(0, 12);
  }

  selectInvestigator(idx: number, inv: InvestigatorMetadata) {
    this.slotOpen = this.slotOpen.map(() => false) as boolean[];

    const placeholder: PoolSlot = {
      code: inv.code,
      name: inv.name,
      faction_code: inv.faction_code ?? 'neutral',
      pool: [],
      loading: true,
    };
    this.slots.update(arr => arr.map((v, i) => i === idx ? placeholder : v));

    this.investigatorService.getInvestigatorCardPool(inv.code).subscribe({
      next: res => {
        this.slots.update(arr => arr.map((v, i) => {
          if (i !== idx || v?.code !== inv.code) return v;
          return { ...placeholder, pool: res.cards, loading: false };
        }));
      },
    });
  }

  removeSlot(idx: number) {
    this.slots.update(arr => arr.map((v, i) => i === idx ? null : v));
    this.invModes.update(m => m.map((v, i) => i === idx ? 'any' : v) as InvMode[]);
  }

  // ── Investigator mode (set algebra) ───────────────────────────────────────

  getInvMode(activeIdx: number): InvMode {
    return this.invModes()[this.activeSlotIndices()[activeIdx]] ?? 'any';
  }

  isIntersectPreset(): boolean {
    const indices = this.activeSlotIndices();
    const modes = this.invModes();
    return this.hasActiveInvFilter() && indices.every(i => modes[i] === 'in');
  }

  isOnlyPreset(activeIdx: number): boolean {
    const indices = this.activeSlotIndices();
    const modes = this.invModes();
    return indices.every((slotIdx, k) =>
      k === activeIdx ? modes[slotIdx] === 'in' : modes[slotIdx] === 'out'
    );
  }

  setInvMode(activeIdx: number, mode: InvMode) {
    const slotIdx = this.activeSlotIndices()[activeIdx];
    this.invModes.update(m => {
      const next = [...m] as InvMode[];
      next[slotIdx] = mode;
      return next;
    });
  }

  applyPreset(type: 'union' | 'intersect' | 'only', activeIdx?: number) {
    const indices = this.activeSlotIndices();
    this.invModes.update(m => {
      const next = [...m] as InvMode[];
      if (type === 'union') {
        indices.forEach(i => next[i] = 'any');
      } else if (type === 'intersect') {
        indices.forEach(i => next[i] = 'in');
      } else if (type === 'only' && activeIdx !== undefined) {
        indices.forEach((i, k) => next[i] = k === activeIdx ? 'in' : 'out');
      }
      return next;
    });
    this.groupPages.set(new Map());
  }

  // ── Multi-select toggles ───────────────────────────────────────────────────

  toggleFilter(sig: ReturnType<typeof signal<Set<string>>>, value: string) {
    sig.update(s => {
      const next = new Set(s);
      next.has(value) ? next.delete(value) : next.add(value);
      return next;
    });
  }

  clearFilters() {
    this.nameSearch.set('');
    this.textSearch.set('');
    this.typeFilter.set(new Set());
    this.factionFilter.set(new Set());
    this.slotFilter.set(new Set());
    this.traitFilter.set(new Set());
    this.packFilter.set(new Set());
    this.costFilter.set(new Set());
    this.xpFilter.set('all');
    this.traitSearchTerm = '';
    this.applyPreset('union');
    this.groupPages.set(new Map());
  }

  // ── Helpers ────────────────────────────────────────────────────────────────

  invImageUrl(code: string): string {
    return `https://arkhamdb.com/bundles/cards/${code}.png`;
  }

  getArkhamIcon(factionCode: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(
      this.arkhamIconsService.getNormalizedIcon(factionCode.toLowerCase())
    );
  }

  xpDots(xp: number): string {
    return '●'.repeat(Math.min(xp, 5));
  }

  splitSlots(real_slot: string | null | undefined): string[] {
    if (!real_slot) return [];
    return real_slot.split('.').map(s => s.trim()).filter(Boolean);
  }

  closeAllDropdowns() {
    this.typeOpen    = false;
    this.factionOpen = false;
    this.slotOpen2   = false;
    this.traitOpen   = false;
    this.packOpen    = false;
    this.costOpen    = false;
  }

  toggleDropdown(name: 'type' | 'faction' | 'slot' | 'trait' | 'pack' | 'cost', event: MouseEvent) {
    event.stopPropagation();
    const wasOpen = name === 'type' ? this.typeOpen
      : name === 'faction' ? this.factionOpen
      : name === 'slot' ? this.slotOpen2
      : name === 'trait' ? this.traitOpen
      : name === 'pack' ? this.packOpen
      : this.costOpen;
    this.closeAllDropdowns();
    if (!wasOpen) {
      if (name === 'type')    this.typeOpen    = true;
      if (name === 'faction') this.factionOpen = true;
      if (name === 'slot')    this.slotOpen2   = true;
      if (name === 'trait')   this.traitOpen   = true;
      if (name === 'pack')    this.packOpen     = true;
      if (name === 'cost')    this.costOpen    = true;
    }
  }

  stopProp(e: MouseEvent) { e.stopPropagation(); }

  @HostListener('document:click')
  onDocumentClick() {
    this.slotOpen = this.slotOpen.map(() => false) as boolean[];
    this.closeAllDropdowns();
  }
}
