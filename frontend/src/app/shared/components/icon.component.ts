import { Component, input, ChangeDetectionStrategy, inject, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IconService } from '../services/icon.service';

/**
 * Optimized icon component with OnPush change detection
 * to prevent unnecessary re-renders
 */
@Component({
  selector: 'app-icon',
  standalone: true,
  imports: [CommonModule],
  template: `<span [innerHTML]="iconHtml()"></span>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class IconComponent {
  name = input.required<string>();

  private iconService = inject(IconService);

  // Use computed to cache the icon HTML based on the name signal
  iconHtml = computed(() => this.iconService.getIcon(this.name()));
}
