import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'arkhamIcons',
  standalone: true
})
export class ArkhamIconsPipe implements PipeTransform {
  
  private iconMap: { [key: string]: string } = {
    // Stats
    '[willpower]': '<span class="icon icon-willpower icon-inline"></span>',
    '[intellect]': '<span class="icon icon-intellect icon-inline"></span>',
    '[combat]': '<span class="icon icon-combat icon-inline"></span>',
    '[agility]': '<span class="icon icon-agility icon-inline"></span>',
    '[wild]': '<span class="icon icon-wild icon-inline"></span>',
    
    // Classes/Factions
    '[guardian]': '<span class="icon icon-guardian icon-inline"></span>',
    '[seeker]': '<span class="icon icon-seeker icon-inline"></span>',
    '[rogue]': '<span class="icon icon-rogue icon-inline"></span>',
    '[mystic]': '<span class="icon icon-mystic icon-inline"></span>',
    '[survivor]': '<span class="icon icon-survivor icon-inline"></span>',
    '[neutral]': '<span class="icon icon-neutral icon-inline"></span>',
    
    // Actions
    '[action]': '<span class="icon icon-action icon-inline"></span>',
    '[reaction]': '<span class="icon icon-reaction icon-inline"></span>',
    '[fast]': '<span class="icon icon-fast icon-inline"></span>',
    '[free]': '<span class="icon icon-free icon-inline"></span>',
    
    // Chaos tokens
    '[skull]': '<span class="icon icon-skull icon-inline"></span>',
    '[cultist]': '<span class="icon icon-cultist icon-inline"></span>',
    '[tablet]': '<span class="icon icon-tablet icon-inline"></span>',
    '[elder_thing]': '<span class="icon icon-elder_thing icon-inline"></span>',
    '[auto_fail]': '<span class="icon icon-auto_fail icon-inline"></span>',
    '[elder_sign]': '<span class="icon icon-elder_sign icon-inline"></span>',
    
    // Other
    '[per_investigator]': '<span class="icon icon-per_investigator icon-inline"></span>',
  };

  constructor(private sanitizer: DomSanitizer) {}

  transform(value: string | null | undefined): SafeHtml {
    if (!value) return '';
    
    let result = value;
    
    // Replace all bracketed icons with HTML spans
    for (const [bracket, html] of Object.entries(this.iconMap)) {
      result = result.split(bracket).join(html);
    }
    
    // Sanitize and return as safe HTML
    return this.sanitizer.bypassSecurityTrustHtml(result);
  }
}

