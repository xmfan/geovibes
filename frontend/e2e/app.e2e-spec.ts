import { GeovibesPage } from './app.po';

describe('geovibes App', function() {
  let page: GeovibesPage;

  beforeEach(() => {
    page = new GeovibesPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
