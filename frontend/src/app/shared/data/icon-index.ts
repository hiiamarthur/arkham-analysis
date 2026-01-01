/**
 * Icon Data Index
 *
 * This file provides convenient access to all Arkham Horror LCG icon data.
 *
 * Total icons: 368
 * - Core icons: 22 (stats, actions, chaos tokens, factions)
 * - Campaign icons: 27
 * - Encounter set icons: 319
 *
 * All icons are automatically extracted from the official Inkscape SVG files.
 */

import { ICON_DATA } from './arkham-icon-data';
import { CAMPAIGN_ICON_DATA } from './campaign-icon-data';
import { ENCOUNTER_ICON_DATA_1 } from './encounter-icon-data-1';
import { ENCOUNTER_ICON_DATA_2 } from './encounter-icon-data-2';
import { ENCOUNTER_ICON_DATA_3 } from './encounter-icon-data-3';
import { ENCOUNTER_ICON_DATA_4 } from './encounter-icon-data-4';
import { ENCOUNTER_ICON_DATA_5 } from './encounter-icon-data-5';
import { ENCOUNTER_ICON_DATA_6 } from './encounter-icon-data-6';
import { ENCOUNTER_ICON_DATA_7 } from './encounter-icon-data-7';

/**
 * All icon data merged into a single object for easy access
 */
export const ALL_ICON_DATA = {
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

/**
 * Export individual data sources for selective importing
 */
export {
  ICON_DATA,
  CAMPAIGN_ICON_DATA,
  ENCOUNTER_ICON_DATA_1,
  ENCOUNTER_ICON_DATA_2,
  ENCOUNTER_ICON_DATA_3,
  ENCOUNTER_ICON_DATA_4,
  ENCOUNTER_ICON_DATA_5,
  ENCOUNTER_ICON_DATA_6,
  ENCOUNTER_ICON_DATA_7
};

export type { IconData } from './arkham-icon-data';
