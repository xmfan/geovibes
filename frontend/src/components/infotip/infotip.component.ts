import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'infotip',
  templateUrl: './infotip.component.html',
  styleUrls: ['./infotip.component.css']
})
export class InfotipComponent implements OnInit {
  example = ['a', 'b'];

  constructor() { }

  ngOnInit() {
  }

}
