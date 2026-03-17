import { Component, Input, Output, EventEmitter, OnInit, OnDestroy, OnChanges, SimpleChanges, signal, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CustomInputComponent } from './text-field.component';
import { CardCodeLinkComponent } from './card-code-link.component';
import { IconService } from '../services/icon.service';
import { SafeHtml, DomSanitizer } from '@angular/platform-browser';

export interface TableColumn {
  key: string;
  label: string;
  sortable?: boolean;
  filterable?: boolean;
  searchable?: boolean;
  visible?: boolean;
  width?: string;
  type?: 'text' | 'number' | 'date' | 'boolean' | 'custom';
  render?: (value: any, row: any) => string;
  /**
   * Responsive priority — controls when the column hides as the viewport narrows:
   *   1 = always visible
   *   2 = hidden below 640px
   *   3 = hidden below 1024px
   * Defaults to 1 if omitted.
   */
  priority?: 1 | 2 | 3;
}

export interface TableConfig {
  pageSize?: number;
  pageSizeOptions?: number[];
  showPagination?: boolean;
  showSearch?: boolean;
  showColumnToggle?: boolean;
  showFilters?: boolean;
  striped?: boolean;
  hoverable?: boolean;
  bordered?: boolean;
  responsive?: boolean;
}

export interface PaginationInfo {
  currentPage: number;
  pageSize: number;
  totalItems: number;
  totalPages: number;
}

@Component({
  selector: 'app-data-table',
  standalone: true,
  imports: [CommonModule, FormsModule, CustomInputComponent, CardCodeLinkComponent],
  templateUrl: './data-table.component.html',
  styleUrl: './data-table.component.css'
})
export class DataTableComponent implements OnInit, OnDestroy, OnChanges {
  @Input() data: any[] = [];
  @Input() columns: TableColumn[] = [];
  @Input() config: TableConfig = {};
  @Input() loading: boolean = false;
  @Input() emptyMessage: string = 'No data available';

  @Output() rowClick = new EventEmitter<any>();
  @Output() pageChange = new EventEmitter<PaginationInfo>();
  @Output() sortChange = new EventEmitter<{column: string, direction: 'asc' | 'desc'}>();
  @Output() filterChange = new EventEmitter<{column: string, value: any}>();

  private iconService = inject(IconService);
  private sanitizer = inject(DomSanitizer);

  // Signals for reactive state
  dataSignal = signal<any[]>([]);
  searchTerm = signal('');
  currentPage = signal(1);
  pageSize = signal(10);
  sortColumn = signal<string | null>(null);
  sortDirection = signal<'asc' | 'desc'>('asc');
  visibleColumns = signal<TableColumn[]>([]);
  filters = signal<Record<string, any>>({});
  columnToggleOpen = false;

  // Computed values
  filteredData = computed(() => {
    let result = [...this.dataSignal()];

    // Apply search
    const search = this.searchTerm();
    if (search) {
      result = result.filter(row =>
        this.columns.some(col => {
          if (!col.searchable) return false;
          const value = this.getCellValue(row, col.key);
          return String(value).toLowerCase().includes(search.toLowerCase());
        })
      );
    }

    // Apply filters
    const activeFilters = this.filters();
    Object.entries(activeFilters).forEach(([column, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        result = result.filter(row => {
          const cellValue = this.getCellValue(row, column);
          return String(cellValue).toLowerCase() === String(value).toLowerCase();
        });
      }
    });

    // Apply sorting
    const sortCol = this.sortColumn();
    const sortDir = this.sortDirection();
    if (sortCol) {
      result.sort((a, b) => {
        const aVal = this.getCellValue(a, sortCol);
        const bVal = this.getCellValue(b, sortCol);

        if (aVal < bVal) return sortDir === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDir === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return result;
  });

  paginatedData = computed(() => {
    const filtered = this.filteredData();
    const page = this.currentPage();
    const size = this.pageSize();
    const start = (page - 1) * size;
    const end = start + size;
    return filtered.slice(start, end);
  });

  paginationInfo = computed(() => {
    const total = this.filteredData().length;
    const size = this.pageSize();
    const current = this.currentPage();
    return {
      currentPage: current,
      pageSize: size,
      totalItems: total,
      totalPages: Math.ceil(total / size)
    };
  });

  // Default configuration
  defaultConfig: TableConfig = {
    pageSize: 10,
    pageSizeOptions: [5, 10, 25, 50, 100],
    showPagination: true,
    showSearch: true,
    showColumnToggle: true,
    showFilters: true,
    striped: true,
    hoverable: true,
    bordered: true,
    responsive: true
  };

  ngOnInit() {
    this.initializeComponent();
    // Initialize data signal with initial data
    this.dataSignal.set(this.data);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['data']) {
      this.dataSignal.set(changes['data'].currentValue || []);
    }
  }

  ngOnDestroy() {
    // Cleanup if needed
  }

  private initializeComponent() {
    // Merge default config with input config
    this.config = { ...this.defaultConfig, ...this.config };
    
    // Set initial page size
    this.pageSize.set(this.config.pageSize || 10);
    
    // Initialize visible columns
    this.updateVisibleColumns();
  }

  private updateVisibleColumns() {
    this.visibleColumns.set(
      this.columns.filter(col => col.visible !== false)
    );
  }

  getCellValue(row: any, key: string): any {
    return key.split('.').reduce((obj, prop) => obj?.[prop], row);
  }

  // Event handlers
  onSearchChange(value: string) {
    this.searchTerm.set(value);
    this.currentPage.set(1); // Reset to first page
  }

  onSort(column: string) {
    const currentSort = this.sortColumn();
    const currentDirection = this.sortDirection();

    if (currentSort === column) {
      // Toggle direction
      this.sortDirection.set(currentDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // New column, start with ascending
      this.sortColumn.set(column);
      this.sortDirection.set('asc');
    }

    this.sortChange.emit({
      column: this.sortColumn()!,
      direction: this.sortDirection()
    });
  }

  onPageChange(page: number) {
    this.currentPage.set(page);
    this.pageChange.emit(this.paginationInfo());
  }

  onPageSizeChange(size: number) {
    this.pageSize.set(size);
    this.currentPage.set(1); // Reset to first page
    this.pageChange.emit(this.paginationInfo());
  }

  onFilterChange(column: string, value: any) {
    const currentFilters = this.filters();
    this.filters.set({ ...currentFilters, [column]: value });
    this.currentPage.set(1); // Reset to first page
    this.filterChange.emit({ column, value });
  }

  onRowClick(row: any) {
    this.rowClick.emit(row);
  }

  toggleColumnVisibility(column: TableColumn) {
    column.visible = !column.visible;
    this.updateVisibleColumns();
  }

  clearFilters() {
    this.filters.set({});
    this.searchTerm.set('');
    this.currentPage.set(1);
  }

  // Get unique filter options for a column
  getFilterOptions(columnKey: string): string[] {
    const uniqueValues = new Set<string>();
    this.dataSignal().forEach(row => {
      const value = this.getCellValue(row, columnKey);
      if (value !== null && value !== undefined && value !== '') {
        uniqueValues.add(String(value));
      }
    });
    return Array.from(uniqueValues).sort();
  }

  // Utility methods
  getSortIcon(column: string): SafeHtml {
    const unsorted = `<svg xmlns="http://www.w3.org/2000/svg" width="12" height="14" viewBox="0 0 12 14" fill="none">
      <path d="M6 1L6 13M6 1L3 4M6 1L9 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.35"/>
      <path d="M6 13L3 10M6 13L9 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.35"/>
    </svg>`;
    const asc = `<svg xmlns="http://www.w3.org/2000/svg" width="12" height="14" viewBox="0 0 12 14" fill="none">
      <path d="M6 2L6 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      <path d="M3 5L6 2L9 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`;
    const desc = `<svg xmlns="http://www.w3.org/2000/svg" width="12" height="14" viewBox="0 0 12 14" fill="none">
      <path d="M6 2L6 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      <path d="M3 9L6 12L9 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`;
    if (this.sortColumn() !== column) return this.sanitizer.bypassSecurityTrustHtml(unsorted);
    return this.sanitizer.bypassSecurityTrustHtml(this.sortDirection() === 'asc' ? asc : desc);
  }

  getPageNumbers(): number[] {
    const info = this.paginationInfo();
    const current = info.currentPage;
    const total = info.totalPages;
    const pages: number[] = [];

    // Always show first page
    if (total > 0) pages.push(1);

    // Show pages around current page
    const start = Math.max(2, current - 2);
    const end = Math.min(total - 1, current + 2);

    if (start > 2) pages.push(-1); // Ellipsis

    for (let i = start; i <= end; i++) {
      pages.push(i);
    }

    if (end < total - 1) pages.push(-1); // Ellipsis

    // Always show last page
    if (total > 1) pages.push(total);

    return pages;
  }

  xpDots(xp: number): string {
    return '●'.repeat(Math.min(xp, 5));
  }

  renderCellValue(row: any, column: TableColumn): string {
    const value = this.getCellValue(row, column.key);

    if (column.render) {
      return column.render(value, row);
    }

    switch (column.type) {
      case 'date':
        return value ? new Date(value).toLocaleDateString() : '';
      case 'boolean':
        return value ? '✓' : '✗';
      case 'number':
        return value?.toLocaleString() || '0';
      default:
        return String(value || '');
    }
  }

  // Check if a column should render as a card code link
  isCardCodeColumn(columnKey: string): boolean {
    return columnKey === 'card_code' || columnKey === 'card1' || columnKey === 'card2';
  }

  // TrackBy function for performance optimization
  trackByFn(index: number, item: any): any {
    return item.id || item.code || index;
  }

  // Get icon from IconService
  getIcon(iconName: string): SafeHtml {
    return this.iconService.getIcon(iconName);
  }

  // Expose Math and Object to template
  Math = Math;
  Object = Object;
}
