import { Component, signal, computed, OnInit, OnDestroy, ViewChild, ElementRef, AfterViewInit, inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Chart, registerables } from 'chart.js';
import { AppStateService } from '../../services/app-state.service';
import { ScenarioService, Scenario, Campaign, DashboardStats, DashboardCard } from '../../services/scenario.service';
import { IconService } from '../../shared/services/icon.service';
import { SafeHtml } from '@angular/platform-browser';

const FACTION_COLORS: Record<string, string> = {
  guardian: '#2b80c5',
  seeker:   '#ec8b26',
  rogue:    '#107116',
  mystic:   '#6c3483',
  survivor: '#cc3038',
  neutral:  '#4a5568',
};

// Cthulhu theme chart defaults
const CHART_TEXT   = '#7c7189';
const CHART_GRID   = 'rgba(201,168,76,0.06)';
const CHART_BORDER = '#0a080f';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild('factionChart',     { static: false }) factionChartRef!:     ElementRef<HTMLCanvasElement>;
  @ViewChild('campaignChart',    { static: false }) campaignChartRef!:    ElementRef<HTMLCanvasElement>;
  @ViewChild('metaFactionChart', { static: false }) metaFactionChartRef!: ElementRef<HTMLCanvasElement>;
  @ViewChild('xpChart',          { static: false }) xpChartRef!:          ElementRef<HTMLCanvasElement>;

  private charts: Chart[] = [];
  private iconService = inject(IconService);
  private platformId = inject(PLATFORM_ID);

  campaigns    = signal<Campaign[]>([]);
  scenarios    = signal<Scenario[]>([]);
  loading      = signal(true);
  dashboardStats  = signal<DashboardStats | null>(null);
  statsLoading    = signal(true);

  traits        = computed(() => this.appState.traits());
  encounterSets = computed(() => this.appState.encounterSets());
  investigators = computed(() => this.appState.investigators());

  traitCount        = computed(() => this.traits().length);
  encounterSetCount = computed(() => this.encounterSets().length);
  investigatorCount = computed(() => this.investigators().length);
  campaignCount     = computed(() => this.campaigns().length);
  scenarioCount     = computed(() => this.scenarios().length);

  factionBreakdown = computed(() => {
    const factions: Record<string, number> = {
      guardian: 0, seeker: 0, rogue: 0, mystic: 0, survivor: 0, neutral: 0
    };
    this.investigators().forEach(i => {
      const f = (i.faction_code ?? 'neutral').toLowerCase();
      if (f in factions) factions[f]++; else factions['neutral']++;
    });
    return factions;
  });

  scenariosPerCampaign = computed(() => ({
    labels: this.campaigns().map(c => c.name),
    data:   this.campaigns().map(c => c.scenario_count ?? c.scenarios ?? 0),
  }));

  quickScenarios = [
    { code: 'the_gathering',       name: 'The Gathering',       campaign: 'Night of the Zealot', note: 'Good starting point' },
    { code: 'curtain_call',        name: 'Curtain Call',        campaign: 'Path to Carcosa',     note: 'Horror-heavy bag' },
    { code: 'a_phantom_of_truth',  name: 'A Phantom of Truth',  campaign: 'Path to Carcosa',     note: 'Variable skull pressure' },
    { code: 'the_boundary_beyond', name: 'The Boundary Beyond', campaign: 'The Forgotten Age',   note: 'Elevated difficulty' },
  ];

  constructor(private appState: AppStateService, private scenarioService: ScenarioService) {
    if (isPlatformBrowser(this.platformId)) Chart.register(...registerables);
  }

  ngOnInit(): void {
    this.loadData();
    this.loadDashboardStats();
  }

  ngAfterViewInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      setTimeout(() => this.buildStaticCharts(), 600);
    }
  }

  ngOnDestroy(): void {
    this.charts.forEach(c => c.destroy());
  }

  // ── Data loading ───────────────────────────────────────────────
  private async loadData(): Promise<void> {
    this.loading.set(true);
    try {
      const [campaigns, scenarios] = await Promise.all([
        this.scenarioService.getCampaigns().toPromise(),
        this.scenarioService.getScenarios().toPromise(),
      ]);
      if (campaigns) this.campaigns.set(campaigns);
      if (scenarios) this.scenarios.set(scenarios);
    } catch (e) {
      console.error('Dashboard load failed:', e);
    } finally {
      this.loading.set(false);
      if (isPlatformBrowser(this.platformId)) setTimeout(() => this.buildStaticCharts(), 100);
    }
  }

  private async loadDashboardStats(): Promise<void> {
    this.statsLoading.set(true);
    try {
      const stats = await this.scenarioService.getDashboardStats(365).toPromise();
      if (stats) {
        this.dashboardStats.set(stats);
        if (isPlatformBrowser(this.platformId)) setTimeout(() => this.buildMetaCharts(), 100);
      }
    } catch (e) {
      console.error('Dashboard stats load failed:', e);
    } finally {
      this.statsLoading.set(false);
    }
  }

  // ── Chart builders ─────────────────────────────────────────────
  private buildStaticCharts(): void {
    this.destroyCharts(['factionChart', 'campaignChart']);
    this.buildFactionChart();
    this.buildCampaignChart();
  }

  private buildMetaCharts(): void {
    this.destroyCharts(['metaFactionChart', 'xpChart']);
    this.buildMetaFactionChart();
    this.buildXpChart();
  }

  private destroyCharts(tags: string[]): void {
    // Chart.js tracks instances by canvas id; destroy all and rebuild selectively
    this.charts = this.charts.filter(c => {
      const id = (c.canvas as HTMLCanvasElement)?.id;
      if (tags.includes(id)) { c.destroy(); return false; }
      return true;
    });
  }

  private buildFactionChart(): void {
    const ctx = this.factionChartRef?.nativeElement?.getContext('2d');
    if (!ctx) return;
    const breakdown = this.factionBreakdown();
    const labels = Object.keys(breakdown).filter(k => breakdown[k] > 0);
    this.charts.push(new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels.map(l => l.charAt(0).toUpperCase() + l.slice(1)),
        datasets: [{
          data: labels.map(k => breakdown[k]),
          backgroundColor: labels.map(k => FACTION_COLORS[k] ?? '#4a5568'),
          borderWidth: 2, borderColor: CHART_BORDER,
          hoverOffset: 4,
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        animation: { animateRotate: true, duration: 900 },
        cutout: '60%',
        plugins: {
          legend: { position: 'bottom', labels: { color: CHART_TEXT, font: { size: 11 }, padding: 10, usePointStyle: true } },
        }
      }
    }));
  }

  private buildCampaignChart(): void {
    const ctx = this.campaignChartRef?.nativeElement?.getContext('2d');
    if (!ctx) return;
    const { labels, data } = this.scenariosPerCampaign();
    if (!labels.length) return;
    this.charts.push(new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{ data, backgroundColor: 'rgba(139,28,28,0.3)', borderColor: 'rgba(139,28,28,0.7)', borderWidth: 1, borderRadius: 3 }]
      },
      options: {
        responsive: true, maintainAspectRatio: false, indexAxis: 'y',
        animation: { duration: 800 },
        plugins: { legend: { display: false } },
        scales: {
          x: { beginAtZero: true, ticks: { color: CHART_TEXT, font: { size: 10 }, stepSize: 1 }, grid: { color: CHART_GRID } },
          y: { ticks: { color: '#d4cfc5', font: { size: 10 }, callback: (_, i) => {
            const name = labels[i] ?? '';
            return name.length > 18 ? name.slice(0, 16) + '…' : name;
          }}, grid: { display: false } }
        }
      }
    }));
  }

  private buildMetaFactionChart(): void {
    const ctx = this.metaFactionChartRef?.nativeElement?.getContext('2d');
    const share = this.dashboardStats()?.faction_meta_share;
    if (!ctx || !share) return;

    const labels = Object.keys(share);
    const data   = labels.map(k => share[k]);
    const colors = labels.map(k => FACTION_COLORS[k] ?? '#4a5568');

    this.charts.push(new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels.map(l => l.charAt(0).toUpperCase() + l.slice(1)),
        datasets: [{
          data,
          backgroundColor: colors,
          borderWidth: 2, borderColor: '#0d1117',
          hoverOffset: 6,
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        animation: { animateRotate: true, duration: 1000 },
        cutout: '68%',
        plugins: {
          legend: { position: 'right', labels: { color: CHART_TEXT, font: { size: 11 }, padding: 12, usePointStyle: true,
            generateLabels: (chart) => {
              const ds = chart.data.datasets[0];
              return (chart.data.labels as string[]).map((label, i) => ({
                text: `${label}  ${data[i]}%`,
                fillStyle: (ds.backgroundColor as string[])[i],
                strokeStyle: CHART_BORDER,
                lineWidth: 1,
                hidden: false,
                index: i,
              }));
            }
          }},
          tooltip: { callbacks: { label: (ctx) => ` ${ctx.label}: ${ctx.parsed}%` } },
        }
      }
    }));
  }

  private buildXpChart(): void {
    const ctx = this.xpChartRef?.nativeElement?.getContext('2d');
    const dist = this.dashboardStats()?.card_stats?.xp_distribution;
    if (!ctx || !dist) return;

    const labels = Object.keys(dist);
    const counts = labels.map(k => dist[k]);
    const xpTotal = counts.reduce((a, b) => a + b, 0) || 1;
    const pcts = counts.map(v => Math.round(v / xpTotal * 100));

    this.charts.push(new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels.map(l => `${l} XP`),
        datasets: [{
          data: pcts,
          backgroundColor: [
            'rgba(74,66,88,0.5)',
            'rgba(201,168,76,0.25)',
            'rgba(201,168,76,0.45)',
            'rgba(139,28,28,0.55)',
          ],
          borderColor: [
            'rgba(74,66,88,0.9)',
            'rgba(201,168,76,0.7)',
            'rgba(201,168,76,0.9)',
            'rgba(139,28,28,0.9)',
          ],
          borderWidth: 1,
          borderRadius: 4,
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        animation: { duration: 900 },
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: (ctx) => ` ${ctx.parsed.y}% of decks` } }
        },
        scales: {
          x: { ticks: { color: '#d4cfc5', font: { size: 11 } }, grid: { display: false } },
          y: { beginAtZero: true, ticks: { color: CHART_TEXT, font: { size: 10 }, callback: (v: any) => `${v}%` }, grid: { color: CHART_GRID } }
        }
      }
    }));
  }

  // ── Helpers ────────────────────────────────────────────────────
  getFactionColor(faction: string): string {
    return FACTION_COLORS[faction?.toLowerCase()] ?? '#4a5568';
  }

  topCardsByType(type: 'top_assets' | 'top_events' | 'top_skills'): DashboardCard[] {
    return this.dashboardStats()?.card_stats?.[type] ?? [];
  }

  maxMetaShare(): number {
    const top = this.dashboardStats()?.top_investigators?.[0];
    return top?.meta_share ?? 1;
  }

  getIcon(iconName: string): SafeHtml {
    return this.iconService.getIcon(iconName);
  }
}
