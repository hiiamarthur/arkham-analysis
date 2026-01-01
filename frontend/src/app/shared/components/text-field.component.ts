import { Component, Input, forwardRef } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

@Component({
  selector: 'app-custom-input',
  templateUrl: './text-field.component.html',
  styleUrl: './text-field.component.css',
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => CustomInputComponent),
      multi: true,
    },
  ],
})
export class CustomInputComponent implements ControlValueAccessor {
  @Input() type: string = 'text';
  @Input() placeholder: string = '';
  @Input() isAllowDecimals: boolean = false;

  value: string | number = '';

  // ControlValueAccessor callbacks
  onChange = (value: any) => {};
  onTouched = () => {};

  onInput(event: Event) {
    let inputValue = (event.target as HTMLInputElement).value;

    if (this.type === 'number' && !this.isAllowDecimals) {
      inputValue = inputValue.replace(/[^0-9]/g, '');
    }

    this.value = inputValue;
    this.onChange(this.value);
  }

  onBlur() {
    this.onTouched();
  }

  // Required by Angular forms API
  writeValue(value: any): void {
    this.value = value || '';
  }
  registerOnChange(fn: any): void {
    this.onChange = fn;
  }
  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }
}
