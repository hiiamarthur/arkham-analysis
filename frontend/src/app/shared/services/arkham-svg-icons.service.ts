import { Injectable } from '@angular/core';
import { ICON_DATA, IconData } from '../data/arkham-icon-data';
import { CAMPAIGN_ICON_DATA } from '../data/campaign-icon-data';
import { ENCOUNTER_ICON_DATA_1 } from '../data/encounter-icon-data-1';
import { ENCOUNTER_ICON_DATA_2 } from '../data/encounter-icon-data-2';
import { ENCOUNTER_ICON_DATA_3 } from '../data/encounter-icon-data-3';
import { ENCOUNTER_ICON_DATA_4 } from '../data/encounter-icon-data-4';
import { ENCOUNTER_ICON_DATA_5 } from '../data/encounter-icon-data-5';
import { ENCOUNTER_ICON_DATA_6 } from '../data/encounter-icon-data-6';
import { ENCOUNTER_ICON_DATA_7 } from '../data/encounter-icon-data-7';

/**
 * Service that provides inline SVG icons for Arkham Horror.
 * Icons extracted from Inkscape SVG files automatically!
 *
 * Total icons: 368
 * - Core icons: 22 (stats, actions, chaos tokens, factions)
 * - Campaign icons: 27
 * - Encounter set icons: 319
 */
@Injectable({
  providedIn: 'root'
})
export class ArkhamSvgIconsService {
  private iconMap: { [key: string]: string } = this.initializeIcons();

  getIcon(iconName: string): string {
    const svg = this.iconMap[iconName.toLowerCase()];
    if (svg) {
      return svg;
    }
    console.warn(`Icon "${iconName}" not found`);
    return this.getDefaultIcon(iconName);
  }

  getAvailableIcons(): string[] {
    return Object.keys(this.iconMap);
  }

  private initializeIcons(): { [key: string]: string } {
    const icons: { [key: string]: string } = {};

    // Merge all icon data sources
    const allIconData = {
      ...ICON_DATA,
      ...CAMPAIGN_ICON_DATA,
      ...ENCOUNTER_ICON_DATA_1,
      ...ENCOUNTER_ICON_DATA_2,
      ...ENCOUNTER_ICON_DATA_3,
      ...ENCOUNTER_ICON_DATA_4,
      ...ENCOUNTER_ICON_DATA_5,
      ...ENCOUNTER_ICON_DATA_6,
      ...ENCOUNTER_ICON_DATA_7
    };

    // Convert all icon data to SVG strings
    for (const [name, data] of Object.entries(allIconData)) {
      icons[name] = this.createSVG(name, data);
    }

    return icons;
  }

  private createSVG(name: string, data: IconData): string {
    const title = name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());

    return `<svg height="1.2em" viewBox="${data.viewBox}" class="arkham-svg-icon" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
      <title>${title}</title>
      <path d="${data.path}" fill="${data.color}"/>
    </svg>`;
  }

  private getDefaultIcon(iconName: string): string {
    return `<svg height="1.2em" viewBox="0 0 100 100" class="arkham-svg-icon" xmlns="http://www.w3.org/2000/svg">
      <title>Missing: ${iconName}</title>
      <circle cx="50" cy="50" r="40" fill="#ccc"/>
      <text x="50" y="60" text-anchor="middle" fill="#666" font-size="30" font-weight="bold">?</text>
    </svg>`;
  }
}
