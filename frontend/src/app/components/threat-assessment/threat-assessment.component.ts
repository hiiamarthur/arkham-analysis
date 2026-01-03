import { Component, signal, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { AnalysisService, ThreatAssessment } from '../../services/analysis.service';
import { ReplacePipe } from '../../pipes/replace.pipe';
import { IconService } from '../../shared/services/icon.service';
import { SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-threat-assessment',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, ReplacePipe],
  templateUrl: './threat-assessment.component.html',
  styleUrl: './threat-assessment.component.css'
})
export class ThreatAssessmentComponent {
  threatForm: FormGroup;
  
  // Signals
  loading = signal(false);
  assessment = signal<ThreatAssessment | null>(null);
  error = signal<string | null>(null);

  // Computed values
  hasAssessment = computed(() => this.assessment() !== null);
  hasError = computed(() => this.error() !== null);
  threatLevel = computed(() => {
    const level = this.assessment()?.threat_assessment?.overall_threat_level || 0;
    if (level < 0.2) return { level: 'Low', color: '#28a745', percentage: level * 100 };
    if (level < 0.4) return { level: 'Moderate', color: '#ffc107', percentage: level * 100 };
    if (level < 0.6) return { level: 'High', color: '#fd7e14', percentage: level * 100 };
    if (level < 0.8) return { level: 'Critical', color: '#dc3545', percentage: level * 100 };
    return { level: 'Extreme', color: '#6f42c1', percentage: level * 100 };
  });

  private iconService = inject(IconService);

  constructor(
    private fb: FormBuilder,
    private analysisService: AnalysisService
  ) {
    this.threatForm = this.fb.group({
      scenario: ['03043'],
      act: [2],
      agenda: [2],
      doomOnAgenda: [5],
      doomThreshold: [8]
    });
  }

  async assessThreat(): Promise<void> {
    if (!this.threatForm.valid) {
      this.error.set('Please fill in all required fields');
      return;
    }

    this.loading.set(true);
    this.error.set(null);
    this.assessment.set(null);

    try {
      const formValue = this.threatForm.value;
      const response = await this.analysisService.getThreatAssessment(
        formValue.scenario,
        formValue.act,
        formValue.agenda,
        formValue.doomOnAgenda,
        formValue.doomThreshold
      ).toPromise();

      if (response) {
        this.assessment.set(response);
      }
    } catch (error: any) {
      this.error.set(error.message || 'Threat assessment failed');
    } finally {
      this.loading.set(false);
    }
  }

  clearAssessment(): void {
    this.assessment.set(null);
    this.error.set(null);
  }

  // Predefined scenarios for quick testing
  loadScenario(scenario: { name: string, code: string, act: number, agenda: number, doomThreshold: number }): void {
    this.threatForm.patchValue({
      scenario: scenario.code,
      act: scenario.act,
      agenda: scenario.agenda,
      doomThreshold: scenario.doomThreshold,
      doomOnAgenda: 0
    });
  }

  presetScenarios = [
    { name: 'Curtain Call', code: '03043', act: 1, agenda: 1, doomThreshold: 6 },
    { name: 'The Last King', code: '03044', act: 1, agenda: 1, doomThreshold: 8 },
    { name: 'Echoes of the Past', code: '03045', act: 1, agenda: 1, doomThreshold: 7 },
    { name: 'The Unspeakable Oath', code: '03046', act: 1, agenda: 1, doomThreshold: 12 }
  ];

  getFactorClass(value: number): string {
    if (value < 0.2) return 'factor-low';
    if (value < 0.4) return 'factor-moderate';
    if (value < 0.6) return 'factor-high';
    if (value < 0.8) return 'factor-critical';
    return 'factor-extreme';
  }

  getRecommendationIcon(): SafeHtml {
    const level = this.threatLevel().level;
    switch (level) {
      case 'Low': return this.iconService.getIcon('check');
      case 'Moderate': return this.iconService.getIcon('threat');
      case 'High': return this.iconService.getIcon('fire');
      case 'Critical': return this.iconService.getIcon('alert');
      case 'Extreme': return this.iconService.getIcon('skull');
      default: return this.iconService.getIcon('question');
    }
  }

  // Get icon from IconService
  getIcon(iconName: string): SafeHtml {
    return this.iconService.getIcon(iconName);
  }

  getRecommendationTitle(): string {
    const level = this.threatLevel().level;
    switch (level) {
      case 'Low': return 'Stable Situation';
      case 'Moderate': return 'Moderate Pressure';
      case 'High': return 'Dangerous Situation';
      case 'Critical': return 'Critical Emergency';
      case 'Extreme': return 'Extreme Emergency';
      default: return 'Unknown';
    }
  }

  getRecommendationText(): string {
    const level = this.threatLevel().level;
    switch (level) {
      case 'Low':
        return 'The situation is under control. Focus on efficient clue gathering and deck setup. Consider taking some risks for optimal plays.';
      case 'Moderate':
        return 'Some pressure is building. Balance efficiency with safety. Prepare defensive options and consider faster clue gathering.';
      case 'High':
        return 'Dangerous situation requires immediate attention. Prioritize survival and threat mitigation. Fast actions and defensive cards are valuable.';
      case 'Critical':
        return 'Critical emergency! Focus entirely on survival and threat elimination. Play conservatively and use emergency resources.';
      case 'Extreme':
        return 'Extreme emergency! All-out survival mode. Use any available resources to prevent defeat. Consider desperate measures.';
      default:
        return 'Unable to determine threat level recommendations.';
    }
  }
}