import { Component, inject, signal, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { IconService } from '../../shared/services/icon.service';
import { SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-navigation',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './navigation.component.html',
  styleUrl: './navigation.component.css'
})
export class NavigationComponent {
  private iconService = inject(IconService);

  menuOpen = signal(false);

  menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: 'dashboard' },
    { path: '/analysis', label: 'Card', icon: 'level_2_bullet_point' },
    { path: '/investigators', label: 'Investigators', icon: 'investigator' },
    { path: '/threat-assessment', label: 'Threat', icon: 'threat' },
    { path: '/pool-playground', label: 'Pool', icon: 'synergy' },
    { path: '/about', label: 'About', icon: 'info' }
  ];

  toggleMenu(): void {
    this.menuOpen.update(v => !v);
  }

  closeMenu(): void {
    this.menuOpen.set(false);
  }

  @HostListener('document:keydown.escape')
  onEscape(): void {
    this.menuOpen.set(false);
  }

  getIcon(iconName: string): SafeHtml {
    return this.iconService.getIcon(iconName);
  }
}