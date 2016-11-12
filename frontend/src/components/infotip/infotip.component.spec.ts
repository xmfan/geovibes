/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { InfotipComponent } from './infotip.component';

describe('InfotipComponent', () => {
  let component: InfotipComponent;
  let fixture: ComponentFixture<InfotipComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InfotipComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InfotipComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
