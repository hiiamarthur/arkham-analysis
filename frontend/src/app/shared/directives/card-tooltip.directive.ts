import { Directive, Input, HostListener, OnDestroy, inject } from '@angular/core';
import { CardTooltipService } from '../services/card-tooltip.service';

@Directive({
  selector: '[cardTooltip]',
  standalone: true,
})
export class CardTooltipDirective implements OnDestroy {
  @Input('cardTooltip') cardCode = '';

  private service = inject(CardTooltipService);
  private timer: ReturnType<typeof setTimeout> | null = null;
  private lastMouseX = 0;
  private lastMouseY = 0;

  @HostListener('mousemove', ['$event'])
  onMouseMove(event: MouseEvent): void {
    this.lastMouseX = event.clientX;
    this.lastMouseY = event.clientY;
  }

  @HostListener('mouseenter', ['$event'])
  onMouseEnter(event: MouseEvent): void {
    if (!this.cardCode) return;
    this.lastMouseX = event.clientX;
    this.lastMouseY = event.clientY;
    this.timer = setTimeout(() => {
      this.service.showTooltip(this.cardCode, this.lastMouseX, this.lastMouseY);
    }, 380);
  }

  @HostListener('mouseleave')
  onMouseLeave(): void {
    this.cancel();
    this.service.hideTooltip();
  }

  ngOnDestroy(): void {
    this.cancel();
    this.service.hideTooltip();
  }

  private cancel(): void {
    if (this.timer !== null) {
      clearTimeout(this.timer);
      this.timer = null;
    }
  }
}
