import {
  Component,
  Input,
  Output,
  EventEmitter,
  signal,
  computed,
  forwardRef,
  HostListener,
  ElementRef,
  inject,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-autocomplete-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => AutocompleteInputComponent),
      multi: true,
    },
  ],
  template: `
    <div class="ac-wrapper" [class.ac-open]="showDropdown()">
      <div class="ac-input-row">
        <input
          class="ac-input"
          type="text"
          [placeholder]="placeholder"
          [value]="currentValue()"
          (input)="onInput($event)"
          (keydown)="onKeydown($event)"
          (focus)="onFocus()"
          (blur)="onBlur()"
          autocomplete="off"
        />
        <button
          *ngIf="currentValue()"
          class="ac-clear"
          type="button"
          tabindex="-1"
          (mousedown)="clear($event)"
          aria-label="Clear">×</button>
      </div>
      <div class="ac-dropdown" *ngIf="showDropdown()" role="listbox">
        <div
          *ngFor="let s of visibleSuggestions(); let i = index"
          class="ac-option"
          [class.ac-option--active]="i === activeIndex()"
          role="option"
          [attr.aria-selected]="i === activeIndex()"
          (mousedown)="selectSuggestion($event, s)"
          [innerHTML]="highlight(s)"
        ></div>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      width: 100%;
      min-width: 0;
    }

    .ac-wrapper {
      position: relative;
      width: 100%;
    }

    .ac-input-row {
      display: flex;
      align-items: center;
      position: relative;
    }

    .ac-input {
      width: 100%;
      padding: 0.5rem 2rem 0.5rem 0.75rem;
      background: var(--surface-primary, #1a1a2e);
      border: 1px solid var(--border-color, rgba(255,255,255,0.15));
      border-radius: 6px;
      color: var(--text-primary, #e8e0d5);
      font-size: 0.875rem;
      font-family: inherit;
      box-sizing: border-box;
      outline: none;
      transition: border-color 0.2s;
    }

    .ac-input:focus {
      border-color: var(--accent-gold, #c9a84c);
    }

    .ac-open .ac-input {
      border-color: var(--accent-gold, #c9a84c);
      border-bottom-left-radius: 0;
      border-bottom-right-radius: 0;
    }

    .ac-clear {
      position: absolute;
      right: 0.5rem;
      background: none;
      border: none;
      color: var(--text-muted, rgba(255,255,255,0.4));
      cursor: pointer;
      font-size: 1rem;
      line-height: 1;
      padding: 0 0.25rem;
      display: flex;
      align-items: center;
    }

    .ac-clear:hover {
      color: var(--text-primary, #e8e0d5);
    }

    .ac-dropdown {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      z-index: 1000;
      background: var(--surface-elevated, #16213e);
      border: 1px solid var(--accent-gold, #c9a84c);
      border-top: none;
      border-bottom-left-radius: 6px;
      border-bottom-right-radius: 6px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
      max-height: 220px;
      overflow-y: auto;
      scrollbar-width: thin;
      scrollbar-color: rgba(201,168,76,0.3) transparent;
    }

    .ac-dropdown::-webkit-scrollbar { width: 4px; }
    .ac-dropdown::-webkit-scrollbar-track { background: transparent; }
    .ac-dropdown::-webkit-scrollbar-thumb { background: rgba(201,168,76,0.3); border-radius: 2px; }

    .ac-option {
      padding: 0.45rem 0.75rem;
      font-size: 0.875rem;
      color: var(--text-primary, #e8e0d5);
      cursor: pointer;
      transition: background 0.12s;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .ac-option:hover,
    .ac-option--active {
      background: rgba(201,168,76,0.15);
    }

    :host ::ng-deep .ac-option mark {
      background: transparent;
      color: var(--accent-gold, #c9a84c);
      font-weight: 600;
    }
  `],
})
export class AutocompleteInputComponent implements ControlValueAccessor {
  @Input() suggestions: string[] = [];
  @Input() placeholder: string = '';
  @Input() maxSuggestions: number = 8;
  @Output() suggestionSelected = new EventEmitter<string>();

  private el = inject(ElementRef);
  private sanitizer = inject(DomSanitizer);

  currentValue = signal('');
  activeIndex = signal(-1);
  isFocused = signal(false);

  visibleSuggestions = computed(() => {
    const term = this.currentValue().toLowerCase().trim();
    if (!term) return [];
    return this.suggestions
      .filter(s => s.toLowerCase().includes(term))
      .slice(0, this.maxSuggestions);
  });

  showDropdown = computed(() => this.isFocused() && this.visibleSuggestions().length > 0);

  private onChange: (v: string) => void = () => {};
  private onTouched: () => void = () => {};

  writeValue(v: string): void {
    this.currentValue.set(v ?? '');
  }

  registerOnChange(fn: (v: string) => void): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: () => void): void {
    this.onTouched = fn;
  }

  onInput(event: Event): void {
    const v = (event.target as HTMLInputElement).value;
    this.currentValue.set(v);
    this.activeIndex.set(-1);
    this.onChange(v);
    this.onTouched();
  }

  onFocus(): void {
    this.isFocused.set(true);
  }

  onBlur(): void {
    // Delay so mousedown on option can fire first
    setTimeout(() => {
      this.isFocused.set(false);
      this.onTouched();
    }, 150);
  }

  onKeydown(event: KeyboardEvent): void {
    const suggestions = this.visibleSuggestions();
    if (!suggestions.length && event.key !== 'Escape') return;

    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        this.activeIndex.set(Math.min(this.activeIndex() + 1, suggestions.length - 1));
        break;
      case 'ArrowUp':
        event.preventDefault();
        this.activeIndex.set(Math.max(this.activeIndex() - 1, -1));
        break;
      case 'Enter':
        if (this.activeIndex() >= 0 && suggestions[this.activeIndex()]) {
          event.preventDefault();
          this.commit(suggestions[this.activeIndex()]);
        }
        break;
      case 'Escape':
        this.isFocused.set(false);
        this.activeIndex.set(-1);
        break;
    }
  }

  selectSuggestion(event: MouseEvent, s: string): void {
    event.preventDefault();
    this.commit(s);
  }

  clear(event: MouseEvent): void {
    event.preventDefault();
    this.currentValue.set('');
    this.activeIndex.set(-1);
    this.onChange('');
    this.onTouched();
    this.suggestionSelected.emit('');
  }

  private commit(s: string): void {
    this.currentValue.set(s);
    this.onChange(s);
    this.onTouched();
    this.isFocused.set(false);
    this.activeIndex.set(-1);
    this.suggestionSelected.emit(s);
  }

  highlight(suggestion: string): SafeHtml {
    const term = this.currentValue().trim();
    const escaped = this.escapeHtml(suggestion);
    if (!term) return this.sanitizer.bypassSecurityTrustHtml(escaped);

    const lower = suggestion.toLowerCase();
    const termLower = term.toLowerCase();
    const idx = lower.indexOf(termLower);
    if (idx === -1) return this.sanitizer.bypassSecurityTrustHtml(escaped);

    const before = this.escapeHtml(suggestion.slice(0, idx));
    const match = this.escapeHtml(suggestion.slice(idx, idx + term.length));
    const after = this.escapeHtml(suggestion.slice(idx + term.length));
    return this.sanitizer.bypassSecurityTrustHtml(`${before}<mark>${match}</mark>${after}`);
  }

  private escapeHtml(s: string): string {
    return s
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: Event): void {
    if (!this.el.nativeElement.contains(event.target)) {
      this.isFocused.set(false);
    }
  }
}
