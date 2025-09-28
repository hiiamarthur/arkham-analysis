import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-navigation',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './navigation.component.html',
  styleUrl: './navigation.component.css'
})
export class NavigationComponent {
  menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/analysis', label: 'Card Analysis', icon: '🃏' },
    { path: '/threat-assessment', label: 'Threat Assessment', icon: '⚠️' },
    { path: '/about', label: 'About', icon: 'ℹ️' }
  ];
}