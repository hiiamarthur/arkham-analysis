import { Component, signal, computed, OnInit, OnDestroy, ViewChild, ElementRef, AfterViewInit, inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Chart, ChartConfiguration, ChartType, registerables } from 'chart.js';
import { CustomInputComponent } from '../../shared/components/text-field.component';
import { DataTableComponent, TableColumn, TableConfig } from '../../shared/components/data-table.component';
import { SharedModule } from '../../shared/shared.module';
import { TableExampleComponent } from '../table-example/table-example.component';
import { AppStateService } from '../../services/app-state.service';
import { IconService } from '../../shared/services/icon.service';
import { SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, CustomInputComponent, DataTableComponent, TableExampleComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit, OnDestroy, AfterViewInit {
  // Chart references
  @ViewChild('analysisChart', { static: false }) analysisChart!: ElementRef<HTMLCanvasElement>;
  @ViewChild('cardPopularityChart', { static: false }) cardPopularityChart!: ElementRef<HTMLCanvasElement>;
  @ViewChild('threatLevelChart', { static: false }) threatLevelChart!: ElementRef<HTMLCanvasElement>;
  @ViewChild('performanceChart', { static: false }) performanceChart!: ElementRef<HTMLCanvasElement>;

  private charts: Chart[] = [];
  // Quick stats - these could be fetched from an API
  totalAnalyses = signal(0);
  recentAnalyses = signal<any[]>([]);
  favoriteCards = signal<string[]>(['01030', '01031', '01032']);

  // Quick action state
  quickCardCode = signal('');

  private iconService = inject(IconService);
  private platformId = inject(PLATFORM_ID);

  constructor(private appState: AppStateService) {
    if (isPlatformBrowser(this.platformId)) {
      Chart.register(...registerables);
    }
  }

  // Global app state - traits and encounter sets (accessed after constructor)
  traits = computed(() => this.appState.traits());
  encounterSets = computed(() => this.appState.encounterSets());
  traitCount = computed(() => this.traits().length);
  encounterSetCount = computed(() => this.encounterSets().length);
  
  // Table data for recent analyses
  recentAnalysesData = signal([
    {
      id: 1,
      cardName: 'Emergency Cache',
      investigator: 'Roland Banks',
      analysisType: 'Resource Management',
      rating: 9.2,
      timestamp: '2024-01-15T10:30:00',
      scenario: 'The Gathering'
    },
    {
      id: 2,
      cardName: 'Machete',
      investigator: 'Roland Banks',
      analysisType: 'Combat Efficiency',
      rating: 8.7,
      timestamp: '2024-01-15T09:15:00',
      scenario: 'The Midnight Masks'
    },
    {
      id: 3,
      cardName: 'Working a Hunch',
      investigator: 'Rex Murphy',
      analysisType: 'Clue Gathering',
      rating: 8.9,
      timestamp: '2024-01-14T16:45:00',
      scenario: 'Extracurricular Activity'
    }
  ]);

  // Table columns for recent analyses
  recentAnalysesColumns: TableColumn[] = [
    { key: 'cardName', label: 'Card', sortable: true, searchable: true },
    { key: 'investigator', label: 'Investigator', sortable: true, filterable: true },
    { key: 'analysisType', label: 'Analysis Type', sortable: true, filterable: true },
    { key: 'rating', label: 'Rating', sortable: true, type: 'number' },
    { key: 'timestamp', label: 'Date', sortable: true, type: 'date' },
    { key: 'scenario', label: 'Scenario', sortable: true, filterable: true }
  ];

  // Table configuration
  tableConfig: TableConfig = {
    pageSize: 5,
    pageSizeOptions: [5, 10, 25],
    showPagination: true,
    showSearch: true,
    showColumnToggle: true,
    showFilters: true,
    striped: true,
    hoverable: true,
    bordered: true,
    responsive: true
  };
  
  // Dashboard stats
  stats = computed(() => ({
    analysesThisWeek: 12,
    averageCardRating: 7.8,
    topInvestigator: 'Roland Banks',
    mostAnalyzedCard: 'Emergency Cache'
  }));

  // Recent activity mock data
  recentActivity = [
    {
      type: 'strength',
      cards: ['Emergency Cache', 'Machete'],
      investigator: 'Roland Banks',
      timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
      result: 'High value in current context'
    },
    {
      type: 'synergy',
      cards: ['Magnifying Glass', 'Working a Hunch'],
      investigator: 'Rex Murphy',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
      result: 'Strong clue-gathering synergy'
    },
    {
      type: 'timing',
      cards: ['Ward of Protection'],
      investigator: 'Agnes Baker',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4), // 4 hours ago
      result: 'Play early for maximum protection'
    }
  ];

  // Featured scenarios
  featuredScenarios = [
    {
      code: '01104',
      name: 'The Gathering',
      campaign: 'Night of the Zealot',
      difficulty: 'Standard',
      description: 'The introductory scenario perfect for testing card analysis'
    },
    {
      code: '02110',
      name: 'Extracurricular Activity',
      campaign: 'The Dunwich Legacy',
      difficulty: 'Hard',
      description: 'Complex scenario with multiple locations and timing challenges'
    },
    {
      code: '03120',
      name: 'Curtain Call',
      campaign: 'The Path to Carcosa',
      difficulty: 'Expert',
      description: 'Horror-focused scenario ideal for sanity management analysis'
    }
  ];

  // Quick analysis suggestions
  analysisTargets = [
    {
      title: 'Resource Management',
      cards: ['Emergency Cache', 'Crack the Case', 'Stand Together'],
      description: 'Analyze economic efficiency in different contexts'
    },
    {
      title: 'Combat Package',
      cards: ['Machete', 'Combat Training', 'Vicious Blow'],
      description: 'Evaluate fighter card synergies and damage output'
    },
    {
      title: 'Investigation Suite',
      cards: ['Magnifying Glass', 'Working a Hunch', 'Drawn to the Flame'],
      description: 'Compare clue-gathering approaches and efficiency'
    }
  ];

  ngOnInit(): void {
    // Chart already registered in constructor
  }

  ngAfterViewInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      setTimeout(() => {
        this.createCharts();
      }, 100);
    }
  }

  ngOnDestroy(): void {
    this.charts.forEach(chart => chart.destroy());
  }

  private createCharts(): void {
    this.createAnalysisTrendChart();
    this.createCardPopularityChart();
    this.createThreatLevelChart();
    this.createPerformanceChart();
  }

  private createAnalysisTrendChart(): void {
    const ctx = this.analysisChart.nativeElement.getContext('2d');
    if (!ctx) return;

    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
          label: 'Card Analyses',
          data: [12, 19, 8, 15, 22, 18, 25],
          borderColor: '#8B4513',
          backgroundColor: 'rgba(139, 69, 19, 0.1)',
          tension: 0.4,
          fill: true
        }, {
          label: 'Threat Assessments',
          data: [8, 12, 6, 10, 15, 12, 18],
          borderColor: '#FFD700',
          backgroundColor: 'rgba(255, 215, 0, 0.1)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Analysis Activity This Week'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          },
          x: {
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          }
        }
      }
    });

    this.charts.push(chart);
  }

  private createCardPopularityChart(): void {
    const ctx = this.cardPopularityChart.nativeElement.getContext('2d');
    if (!ctx) return;

    const chart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Emergency Cache', 'Machete', 'Working a Hunch', 'Ward of Protection', 'Other'],
        datasets: [{
          data: [25, 20, 18, 15, 22],
          backgroundColor: [
            '#8B4513',
            '#FFD700',
            '#4A2C1A',
            '#CD853F',
            '#DEB887'
          ],
          borderWidth: 2,
          borderColor: '#fff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
          },
          title: {
            display: true,
            text: 'Most Analyzed Cards'
          }
        }
      }
    });

    this.charts.push(chart);
  }

  private createThreatLevelChart(): void {
    const ctx = this.threatLevelChart.nativeElement.getContext('2d');
    if (!ctx) return;

    const chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Low', 'Medium', 'High', 'Critical'],
        datasets: [{
          label: 'Threat Assessments',
          data: [35, 45, 25, 15],
          backgroundColor: [
            '#28a745',
            '#ffc107',
            '#fd7e14',
            '#dc3545'
          ],
          borderColor: [
            '#28a745',
            '#ffc107',
            '#fd7e14',
            '#dc3545'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          title: {
            display: true,
            text: 'Threat Level Distribution'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          },
          x: {
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          }
        }
      }
    });

    this.charts.push(chart);
  }

  private createPerformanceChart(): void {
    const ctx = this.performanceChart.nativeElement.getContext('2d');
    if (!ctx) return;

    const chart = new Chart(ctx, {
      type: 'radar',
      data: {
        labels: ['Analysis Speed', 'Accuracy', 'Context Awareness', 'Threat Detection', 'Card Synergy', 'Strategic Value'],
        datasets: [{
          label: 'System Performance',
          data: [85, 92, 88, 90, 86, 91],
          borderColor: '#8B4513',
          backgroundColor: 'rgba(139, 69, 19, 0.2)',
          borderWidth: 2,
          pointBackgroundColor: '#8B4513',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: '#8B4513'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Analysis System Performance'
          },
          legend: {
            display: false
          }
        },
        scales: {
          r: {
            beginAtZero: true,
            max: 100,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            angleLines: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          }
        }
      }
    });

    this.charts.push(chart);
  }

  // Methods
  analyzeQuickCard(): void {
    if (this.quickCardCode().trim()) {
      // Navigate to analysis with pre-filled card
      // This would be implemented with router navigation
      console.log('Quick analyzing card:', this.quickCardCode());
    }
  }

  getTimeAgo(timestamp: Date): string {
    const now = new Date();
    const diffMs = now.getTime() - timestamp.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMins / 60);
    
    if (diffMins < 60) {
      return `${diffMins} minutes ago`;
    } else if (diffHours < 24) {
      return `${diffHours} hours ago`;
    } else {
      const diffDays = Math.floor(diffHours / 24);
      return `${diffDays} days ago`;
    }
  }

  getAnalysisTypeIcon(type: string): SafeHtml {
    switch (type) {
      case 'strength': return this.iconService.getIcon('strength');
      case 'synergy': return this.iconService.getIcon('synergy');
      case 'timing': return this.iconService.getIcon('timing');
      default: return this.iconService.getIcon('analysis');
    }
  }

  // Get icon from IconService
  getIcon(iconName: string): SafeHtml {
    return this.iconService.getIcon(iconName);
  }

  getDifficultyColor(difficulty: string): string {
    switch (difficulty.toLowerCase()) {
      case 'easy': return '#28a745';
      case 'standard': return '#ffc107';
      case 'hard': return '#fd7e14';
      case 'expert': return '#dc3545';
      default: return '#6c757d';
    }
  }

  // Table event handlers
  onTableRowClick(row: any) {
    console.log('Table row clicked:', row);
    // Navigate to card analysis or show details
  }

  onTablePageChange(paginationInfo: any) {
    console.log('Table page changed:', paginationInfo);
  }

  onTableSortChange(sortInfo: any) {
    console.log('Table sort changed:', sortInfo);
  }

  onTableFilterChange(filterInfo: any) {
    console.log('Table filter changed:', filterInfo);
  }
}