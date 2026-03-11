import { Component, inject } from '@angular/core';
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

  menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: 'dashboard' },
    { path: '/analysis', label: 'Card Analysis', icon: 'level_2_bullet_point' },
    { path: '/investigators', label: 'Investigators', icon: 'investigator' },
    { path: '/threat-assessment', label: 'Threat Assessment', icon: 'threat' },
    { path: '/about', label: 'About', icon: 'info' }
  ];

  getIcon(iconName: string): SafeHtml {
    return this.iconService.getIcon(iconName);
  }
}