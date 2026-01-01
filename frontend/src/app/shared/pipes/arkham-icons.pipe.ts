import { Pipe, PipeTransform, inject } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { ArkhamSvgIconsService } from '../services/arkham-svg-icons.service';

/**
 * Pipe to transform Arkham Horror card text tokens into icons
 * Replaces [token_name] with appropriate SVG icons
 *
 * Usage modes:
 * - 'svg' (default): Uses SVG icons from Inkscape
 * - 'font': Uses icon font (legacy)
 * - 'emoji': Uses Unicode emojis (fallback)
 */
@Pipe({
  name: 'arkhamIcons',
  standalone: true
})
export class ArkhamIconsPipe implements PipeTransform {
  private svgIconsService = inject(ArkhamSvgIconsService);
  private sanitizer = inject(DomSanitizer);
  // Icon mapping - using Unicode characters and emojis
  private iconMap: { [key: string]: string } = {
    // Stats
    'willpower': '🔵',
    'intellect': '🟢',
    'combat': '⚔️',
    'agility': '🟡',
    'wild': '⭐',

    // Actions
    'action': '⚡',
    'reaction': '↩️',
    'free': '🆓',
    'fast': '⚡',

    // Chaos tokens
    'elder_sign': '✨',
    'skull': '💀',
    'cultist': '🎭',
    'tablet': '📜',
    'elder_thing': '🐙',
    'auto_fail': '❌',
    'bless': '✨',
    'curse': '🌙',

    // Other
    'per_investigator': '👤',
    'codex': '📖',
    'guardian': '🛡️',
    'seeker': '🔍',
    'rogue': '🗡️',
    'mystic': '🔮',
    'survivor': '❤️',
    'neutral': '⚪'
  };

  // Font-based icon mapping
  // These use CSS classes that render icons via @font-face and ::before pseudo-elements
  // NO emoji characters needed - the font file provides the glyphs
  private iconMapWithClasses: { [key: string]: string } = {
    // Stats
    'willpower': '<span class="arkham-icon arkham-willpower" title="Willpower"></span>',
    'intellect': '<span class="arkham-icon arkham-intellect" title="Intellect"></span>',
    'combat': '<span class="arkham-icon arkham-combat" title="Combat"></span>',
    'agility': '<span class="arkham-icon arkham-agility" title="Agility"></span>',
    'wild': '<span class="arkham-icon arkham-wild" title="Wild"></span>',

    // Actions
    'action': '<span class="arkham-icon arkham-action" title="Action"></span>',
    'reaction': '<span class="arkham-icon arkham-reaction" title="Reaction"></span>',
    'free': '<span class="arkham-icon arkham-free" title="Free"></span>',
    'fast': '<span class="arkham-icon arkham-fast" title="Fast"></span>',

    // Chaos tokens
    'elder_sign': '<span class="arkham-icon arkham-elder-sign" title="Elder Sign"></span>',
    'skull': '<span class="arkham-icon arkham-skull" title="Skull"></span>',
    'cultist': '<span class="arkham-icon arkham-cultist" title="Cultist"></span>',
    'tablet': '<span class="arkham-icon arkham-tablet" title="Tablet"></span>',
    'elder_thing': '<span class="arkham-icon arkham-elder-thing" title="Elder Thing"></span>',
    'auto_fail': '<span class="arkham-icon arkham-auto-fail" title="Auto-fail"></span>',
    'bless': '<span class="arkham-icon arkham-bless" title="Bless"></span>',
    'curse': '<span class="arkham-icon arkham-curse" title="Curse"></span>',

    // Other
    'per_investigator': '<span class="arkham-icon arkham-per-investigator" title="Per Investigator"></span>',
    'codex': '<span class="arkham-icon arkham-codex" title="Codex"></span>',
    'guardian': '<span class="arkham-icon arkham-guardian" title="Guardian"></span>',
    'seeker': '<span class="arkham-icon arkham-seeker" title="Seeker"></span>',
    'rogue': '<span class="arkham-icon arkham-rogue" title="Rogue"></span>',
    'mystic': '<span class="arkham-icon arkham-mystic" title="Mystic"></span>',
    'survivor': '<span class="arkham-icon arkham-survivor" title="Survivor"></span>',
    'neutral': '<span class="arkham-icon arkham-neutral" title="Neutral"></span>'
  };

  /**
   * Transform card text by replacing [token] patterns with icons
   *
   * @param text - The text to transform
   * @param mode - Icon mode: 'svg' (default), 'font', or 'emoji'
   * @returns Transformed text with icons as SafeHtml
   */
  transform(text: string | null | undefined, mode: 'svg' | 'font' | 'emoji' = 'svg'): SafeHtml {
    if (!text) return '';

    let result = text;

    // First replace [token] patterns with brackets (if any)
    result = result.replace(/\[([a-z_]+)\]/gi, (match, token) => {
      const lowerToken = token.toLowerCase();

      switch (mode) {
        case 'svg':
          return this.svgIconsService.getIcon(lowerToken);

        case 'font':
          return this.iconMapWithClasses[lowerToken] || match;

        case 'emoji':
          return this.iconMap[lowerToken] || match;

        default:
          return match;
      }
    });

    // Also replace standalone icon names (without brackets)
    // Matches words like "Willpower", "Intellect", "Reaction", etc. at word boundaries
    const iconPattern = /\b(willpower|intellect|combat|agility|wild|action|reaction|free|fast|skull|cultist|tablet|elder_thing|elder_sign|auto_fail|bless|curse|per_investigator|guardian|seeker|rogue|mystic|survivor|neutral|codex)\b/gi;

    result = result.replace(iconPattern, (match) => {
      const lowerToken = match.toLowerCase();

      switch (mode) {
        case 'svg':
          return this.svgIconsService.getIcon(lowerToken);

        case 'font':
          return this.iconMapWithClasses[lowerToken] || match;

        case 'emoji':
          return this.iconMap[lowerToken] || match;

        default:
          return match;
      }
    });

    return this.sanitizer.bypassSecurityTrustHtml(result);
  }
}
