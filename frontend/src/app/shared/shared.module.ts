import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ArkhamIconsPipe } from './pipes/arkham-icons.pipe';
import { CardCodeLinkComponent } from './components/card-code-link.component';
import { CardModalComponent } from './components/card-modal.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    ArkhamIconsPipe,
    CardCodeLinkComponent,
    CardModalComponent
  ],
  exports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    ArkhamIconsPipe,
    CardCodeLinkComponent,
    CardModalComponent
  ]
})
export class SharedModule {}