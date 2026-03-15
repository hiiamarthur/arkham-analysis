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
  input,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

@Component({
  selector: 'app-searchable-select',
  standalone: true,
  imports: [CommonModule, FormsModule],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => SearchableSelectComponent),
      multi: true,
    },
  ],
  template: `
    <div class="ss-wrapper" [class.ss-open]="isOpen()" [class.ss-disabled]="isDisabled">
      <!-- Trigger -->
      <button
        type="button"
        class="ss-trigger"
        (click)="toggleDropdown()"
        [disabled]="isDisabled"
        [attr.aria-expanded]="isOpen()"
        [attr.aria-haspopup]="'listbox'">
        <span class="ss-trigger-label" [class.ss-placeholder]="!selectedLabel()">
          {{ selectedLabel() || placeholder }}
        </span>
        <span class="ss-arrow" [class.ss-arrow--up]="isOpen()">&#9660;</span>
      </button>

      <!-- Dropdown -->
      <div class="ss-dropdown" *ngIf="isOpen()" role="listbox">
        <div class="ss-search-wrap">
          <input
            #searchInput
            class="ss-search"
            type="text"
            [placeholder]="searchPlaceholder"
            [ngModel]="searchText()"
            (ngModelChange)="searchText.set($event)"
            (click)="$event.stopPropagation()"
            autocomplete="off"
          />
        </div>
        <div class="ss-options-list">
          <div
            *ngIf="!resetAfterSelect && allowEmpty"
            class="ss-option ss-option-empty"
            [class.ss-option--selected]="selectedValue() === ''"
            (click)="selectOption('')"
            role="option">
            {{ placeholder }}
          </div>
          <div
            *ngFor="let opt of filteredOptions()"
            class="ss-option"
            [class.ss-option--selected]="opt.value === selectedValue()"
            [class.ss-option--disabled]="opt.disabled"
            (click)="!opt.disabled && selectOption(opt.value)"
            role="option"
            [attr.aria-selected]="opt.value === selectedValue()"
            [attr.aria-disabled]="opt.disabled">
            {{ opt.label }}
          </div>
          <div *ngIf="filteredOptions().length === 0" class="ss-no-results">
            No results
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .ss-wrapper {
      position: relative;
      width: 100%;
    }

    .ss-trigger {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      padding: 0.5rem 0.75rem;
      background: var(--surface-primary, #1a1a2e);
      border: 1px solid var(--border-color, rgba(255,255,255,0.15));
      border-radius: 6px;
      color: var(--text-primary, #e8e0d5);
      font-size: 0.875rem;
      cursor: pointer;
      text-align: left;
      transition: border-color 0.2s;
      font-family: inherit;
    }

    .ss-trigger:hover:not(:disabled) {
      border-color: var(--accent-gold, #c9a84c);
    }

    .ss-trigger:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .ss-open .ss-trigger {
      border-color: var(--accent-gold, #c9a84c);
    }

    .ss-trigger-label {
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .ss-placeholder {
      color: var(--text-muted, rgba(255,255,255,0.4));
    }

    .ss-arrow {
      margin-left: 0.5rem;
      font-size: 0.65rem;
      opacity: 0.6;
      transition: transform 0.2s;
      flex-shrink: 0;
    }

    .ss-arrow--up {
      transform: rotate(180deg);
    }

    .ss-dropdown {
      position: absolute;
      top: calc(100% + 4px);
      left: 0;
      right: 0;
      z-index: 1000;
      background: var(--surface-elevated, #16213e);
      border: 1px solid var(--accent-gold, #c9a84c);
      border-radius: 6px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
      overflow: hidden;
    }

    .ss-search-wrap {
      padding: 0.5rem;
      border-bottom: 1px solid var(--border-color, rgba(255,255,255,0.1));
    }

    .ss-search {
      width: 100%;
      padding: 0.375rem 0.5rem;
      background: var(--surface-primary, #1a1a2e);
      border: 1px solid var(--border-color, rgba(255,255,255,0.15));
      border-radius: 4px;
      color: var(--text-primary, #e8e0d5);
      font-size: 0.8rem;
      font-family: inherit;
      box-sizing: border-box;
      outline: none;
    }

    .ss-search:focus {
      border-color: var(--accent-gold, #c9a84c);
    }

    .ss-options-list {
      max-height: 220px;
      overflow-y: auto;
      scrollbar-width: thin;
      scrollbar-color: rgba(201,168,76,0.3) transparent;
    }

    .ss-options-list::-webkit-scrollbar { width: 4px; }
    .ss-options-list::-webkit-scrollbar-track { background: transparent; }
    .ss-options-list::-webkit-scrollbar-thumb { background: rgba(201,168,76,0.3); border-radius: 2px; }

    .ss-option {
      padding: 0.5rem 0.75rem;
      font-size: 0.875rem;
      color: var(--text-primary, #e8e0d5);
      cursor: pointer;
      transition: background 0.15s;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .ss-option:hover:not(.ss-option--disabled) {
      background: rgba(201,168,76,0.12);
    }

    .ss-option--selected {
      background: rgba(201,168,76,0.2);
      color: var(--accent-gold, #c9a84c);
    }

    .ss-option--disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }

    .ss-option-empty {
      color: var(--text-muted, rgba(255,255,255,0.4));
      font-style: italic;
    }

    .ss-no-results {
      padding: 0.75rem;
      text-align: center;
      color: var(--text-muted, rgba(255,255,255,0.4));
      font-size: 0.8rem;
      font-style: italic;
    }
  `],
})
export class SearchableSelectComponent implements ControlValueAccessor {
  options = input<SelectOption[]>([]);
  @Input() placeholder: string = 'Select...';
  @Input() searchPlaceholder: string = 'Search...';
  @Input() allowEmpty: boolean = true;
  /** When true, resets to placeholder after selection (for one-shot pickers) */
  @Input() resetAfterSelect: boolean = false;
  /** Direct disabled input (supplements ControlValueAccessor setDisabledState) */
  @Input() set disabled(val: boolean) { this.isDisabled = val; }
  /** Emit selected value for non-reactive-form use */
  @Output() selected = new EventEmitter<string>();

  private el = inject(ElementRef);

  searchText = signal('');
  isOpen = signal(false);
  selectedValue = signal<string>('');
  isDisabled = false;

  filteredOptions = computed(() => {
    const search = this.searchText().toLowerCase().trim();
    const opts = this.options();
    if (!search) return opts;
    return opts.filter(o => o.label.toLowerCase().includes(search));
  });

  selectedLabel = computed(() => {
    if (this.resetAfterSelect) return '';
    const val = this.selectedValue();
    const opt = this.options().find(o => o.value === val);
    return opt ? opt.label : '';
  });

  private onChange: (value: string) => void = () => {};
  private onTouched: () => void = () => {};

  writeValue(value: string): void {
    this.selectedValue.set(value ?? '');
  }

  registerOnChange(fn: (value: string) => void): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: () => void): void {
    this.onTouched = fn;
  }

  setDisabledState(isDisabled: boolean): void {
    this.isDisabled = isDisabled;
  }

  toggleDropdown(): void {
    if (this.isDisabled) return;
    this.isOpen.update(v => !v);
    if (this.isOpen()) {
      this.searchText.set('');
    }
  }

  selectOption(value: string): void {
    if (this.resetAfterSelect) {
      this.selected.emit(value);
      this.isOpen.set(false);
      this.searchText.set('');
      return;
    }
    this.selectedValue.set(value);
    this.onChange(value);
    this.onTouched();
    this.selected.emit(value);
    this.isOpen.set(false);
    this.searchText.set('');
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: Event): void {
    if (!this.el.nativeElement.contains(event.target)) {
      this.isOpen.set(false);
    }
  }
}
