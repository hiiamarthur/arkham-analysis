import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DataTableComponent, TableColumn, TableConfig } from '../../shared/components/data-table.component';

@Component({
  selector: 'app-table-example',
  standalone: true,
  imports: [CommonModule, DataTableComponent],
  template: `
    <div class="example-container">
      <h2>Data Table Example</h2>
      
      <app-data-table
        [data]="sampleData()"
        [columns]="columns"
        [config]="tableConfig"
        [loading]="loading()"
        (rowClick)="onRowClick($event)"
        (pageChange)="onPageChange($event)"
        (sortChange)="onSortChange($event)"
        (filterChange)="onFilterChange($event)"
      ></app-data-table>
    </div>
  `,
  styles: [`
    .example-container {
      padding: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }
    
    h2 {
      margin-bottom: 2rem;
      color: #8B4513;
    }
  `]
})
export class TableExampleComponent {
  loading = signal(false);

  // Sample data
  sampleData = signal([
    {
      id: 1,
      name: 'Emergency Cache',
      type: 'Asset',
      cost: 0,
      faction: 'Neutral',
      pack: 'Core Set',
      popularity: 95,
      lastUpdated: '2024-01-15',
      isActive: true
    },
    {
      id: 2,
      name: 'Machete',
      type: 'Asset',
      cost: 3,
      faction: 'Guardian',
      pack: 'Core Set',
      popularity: 88,
      lastUpdated: '2024-01-14',
      isActive: true
    },
    {
      id: 3,
      name: 'Working a Hunch',
      type: 'Event',
      cost: 1,
      faction: 'Seeker',
      pack: 'Core Set',
      popularity: 82,
      lastUpdated: '2024-01-13',
      isActive: false
    },
    {
      id: 4,
      name: 'Ward of Protection',
      type: 'Event',
      cost: 1,
      faction: 'Mystic',
      pack: 'Core Set',
      popularity: 90,
      lastUpdated: '2024-01-12',
      isActive: true
    },
    {
      id: 5,
      name: 'Magnifying Glass',
      type: 'Asset',
      cost: 2,
      faction: 'Seeker',
      pack: 'Core Set',
      popularity: 85,
      lastUpdated: '2024-01-11',
      isActive: true
    }
  ]);

  // Column definitions
  columns: TableColumn[] = [
    {
      key: 'id',
      label: 'ID',
      sortable: true,
      filterable: true,
      searchable: true,
      type: 'number',
      width: '80px'
    },
    {
      key: 'name',
      label: 'Card Name',
      sortable: true,
      filterable: true,
      searchable: true,
      type: 'text'
    },
    {
      key: 'type',
      label: 'Type',
      sortable: true,
      filterable: true,
      searchable: true,
      type: 'text',
      width: '100px'
    },
    {
      key: 'cost',
      label: 'Cost',
      sortable: true,
      filterable: true,
      type: 'number',
      width: '80px'
    },
    {
      key: 'faction',
      label: 'Faction',
      sortable: true,
      filterable: true,
      searchable: true,
      type: 'text',
      width: '100px'
    },
    {
      key: 'pack',
      label: 'Pack',
      sortable: true,
      filterable: true,
      searchable: true,
      type: 'text',
      width: '120px'
    },
    {
      key: 'popularity',
      label: 'Popularity',
      sortable: true,
      filterable: true,
      type: 'number',
      width: '100px',
      render: (value: number) => `${value}%`
    },
    {
      key: 'lastUpdated',
      label: 'Last Updated',
      sortable: true,
      filterable: true,
      type: 'date',
      width: '120px'
    },
    {
      key: 'isActive',
      label: 'Active',
      sortable: true,
      filterable: true,
      type: 'boolean',
      width: '80px'
    }
  ];

  // Table configuration
  tableConfig: TableConfig = {
    pageSize: 5,
    pageSizeOptions: [5, 10, 25, 50],
    showPagination: true,
    showSearch: true,
    showColumnToggle: true,
    showFilters: true,
    striped: true,
    hoverable: true,
    bordered: true,
    responsive: true
  };

  // Event handlers
  onRowClick(row: any) {
    alert(`Clicked on: ${row.name}`);
  }

  onPageChange(paginationInfo: any) {
  }

  onSortChange(sortInfo: any) {
  }

  onFilterChange(filterInfo: any) {
  }
}
