/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { WorldmapComponent } from './worldmap.component';

describe('WorldmapComponent', () => {
  let component: WorldmapComponent;
  let fixture: ComponentFixture<WorldmapComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WorldmapComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WorldmapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
