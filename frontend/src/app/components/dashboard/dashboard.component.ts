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
      // Wait for view to be fully initialized
      setTimeout(() => {
        console.log('=== Starting Chart Initialization ===');
        console.log('analysisChart element:', this.analysisChart?.nativeElement);
        console.log('threatLevelChart element:', this.threatLevelChart?.nativeElement);
        console.log('cardPopularityChart element:', this.cardPopularityChart?.nativeElement);
        console.log('performanceChart element:', this.performanceChart?.nativeElement);

        this.createCharts();

        console.log('=== Charts Created ===');
        console.log('Total charts:', this.charts.length);
        this.charts.forEach((chart, index) => {
          console.log(`Chart ${index}:`, 'canvas:', chart.canvas.width, 'x', chart.canvas.height);
        });
      }, 500);
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
    if (!ctx) {
      console.error('Analysis Trend Chart: Canvas context not available');
      return;
    }

    console.log('Creating Analysis Trend Chart...');
    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
          label: 'Card Analyses',
          data: [12, 19, 8, 15, 22, 18, 25],
          borderColor: '#3a5a4a',
          backgroundColor: 'rgba(58, 90, 74, 0.2)',
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          pointRadius: 5,
          pointHoverRadius: 7,
          pointBackgroundColor: '#3a5a4a',
          pointBorderColor: '#c8d3d5',
          pointBorderWidth: 2
        }, {
          label: 'Threat Assessments',
          data: [8, 12, 6, 10, 15, 12, 18],
          borderColor: '#6a8a7a',
          backgroundColor: 'rgba(106, 138, 122, 0.2)',
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          pointRadius: 5,
          pointHoverRadius: 7,
          pointBackgroundColor: '#6a8a7a',
          pointBorderColor: '#c8d3d5',
          pointBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: '#c8d3d5',
              font: {
                size: 12
              },
              usePointStyle: true,
              padding: 15
            }
          },
          title: {
            display: true,
            text: 'Analysis Activity This Week',
            color: '#c8d3d5',
            font: {
              size: 14,
              weight: 'bold'
            },
            padding: {
              bottom: 20
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            suggestedMax: 30,
            ticks: {
              color: '#7a8a8c',
              stepSize: 5,
              font: {
                size: 11
              }
            },
            grid: {
              color: 'rgba(58, 90, 74, 0.3)',
              lineWidth: 1
            }
          },
          x: {
            ticks: {
              color: '#7a8a8c',
              font: {
                size: 11
              }
            },
            grid: {
              color: 'rgba(58, 90, 74, 0.2)',
              lineWidth: 1
            }
          }
        },
        interaction: {
          intersect: false,
          mode: 'index'
        }
      }
    });

    console.log('Analysis Trend Chart created with data:', chart.data.datasets.map(d => d.data));
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
            '#3a5a4a',
            '#2d4d3d',
            '#4a6a5a',
            '#5a7a6a',
            '#1a4d3d'
          ],
          borderWidth: 2,
          borderColor: '#0a0a0f'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#c8d3d5',
              font: {
                size: 11
              },
              padding: 10
            }
          },
          title: {
            display: true,
            text: 'Most Analyzed Cards',
            color: '#c8d3d5',
            font: {
              size: 14
            }
          }
        }
      }
    });

    this.charts.push(chart);
  }

  private createThreatLevelChart(): void {
    console.log('--- Creating Threat Level Chart ---');
    const canvas = this.threatLevelChart.nativeElement;
    console.log('Canvas element:', canvas);
    console.log('Canvas dimensions:', canvas.width, 'x', canvas.height);

    const ctx = canvas.getContext('2d');
    if (!ctx) {
      console.error('Threat Level Chart: Canvas context not available');
      return;
    }
    console.log('Canvas context obtained:', ctx);

    const data = [35, 45, 25, 15];
    console.log('Bar chart data:', data);

    const chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Low', 'Medium', 'High', 'Critical'],
        datasets: [{
          label: 'Threat Assessments',
          data: data,
          backgroundColor: [
            '#2d5d4d',
            '#5a7a4a',
            '#7a6a3a',
            '#7a4a3a'
          ],
          borderColor: [
            '#3a6a5a',
            '#6a8a5a',
            '#8a7a4a',
            '#8a5a4a'
          ],
          borderWidth: 2
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
            text: 'Threat Level Distribution',
            color: '#c8d3d5',
            font: {
              size: 16,
              weight: 'bold'
            },
            padding: {
              bottom: 10
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 50,
            ticks: {
              color: '#7a8a8c',
              stepSize: 10,
              font: {
                size: 12
              }
            },
            grid: {
              color: 'rgba(58, 90, 74, 0.4)',
              lineWidth: 1
            }
          },
          x: {
            ticks: {
              color: '#7a8a8c',
              font: {
                size: 12
              }
            },
            grid: {
              display: false
            }
          }
        }
      }
    });

    console.log('Threat Level Chart created successfully');
    console.log('Chart instance:', chart);
    console.log('Chart canvas after creation:', chart.canvas.width, 'x', chart.canvas.height);
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
          borderColor: '#3a5a4a',
          backgroundColor: 'rgba(58, 90, 74, 0.3)',
          borderWidth: 2,
          pointBackgroundColor: '#3a5a4a',
          pointBorderColor: '#c8d3d5',
          pointHoverBackgroundColor: '#c8d3d5',
          pointHoverBorderColor: '#3a5a4a'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Analysis System Performance',
            color: '#c8d3d5',
            font: {
              size: 14
            }
          },
          legend: {
            display: false
          }
        },
        scales: {
          r: {
            beginAtZero: true,
            max: 100,
            ticks: {
              color: '#7a8a8c',
              backdropColor: 'transparent'
            },
            pointLabels: {
              color: '#7a8a8c',
              font: {
                size: 10
              }
            },
            grid: {
              color: 'rgba(58, 90, 74, 0.3)'
            },
            angleLines: {
              color: 'rgba(58, 90, 74, 0.3)'
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