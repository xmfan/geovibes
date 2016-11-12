import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { PopoverModule } from 'ng2-popover';

import { AppComponent } from './app.component';
import { InfotipComponent } from '../components/infotip/infotip.component';

@NgModule({
  declarations: [
    AppComponent,
    InfotipComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    PopoverModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
