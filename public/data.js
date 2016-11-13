var data;
var article_map = new Map();

$(function() {
  initMap();
  $("#chartdiv").on('click', function() {
    hideNewsPanel();
  });
});

function initMap() {
  $.get('sample.js'/*"http://10.8.86.139:5000/events"*/, function(res) {
    // articles_array = JSON.parse(res).response;
    articles_array = data.response;
    generateMap(generateImages(articles_array));
    $('a[title="Interactive JavaScript maps"]').remove(); // remove watermark
  });
}

function generateImages(articles) {
  var images = [];

  for (var i in articles) {
    var article = articles[i];

    images.push({
      "svgPath": targetSVG,
      "zoomLevel": 5,
      "scale": 0.5,
      "title": article.name,
      "latitude": article.lat,
      "longitude": article.long
    });

    article_map.set(article.name, article);
  }

  return images;
}

function generateMap(images) {
  map = AmCharts.makeChart("chartdiv", {
    "type": "map",
    "projection": "eckert5",
    "theme": "light",
    "imagesSettings": {
      "rollOverColor": "#089282",
      "rollOverScale": 3,
      "selectedScale": 3,
      "selectedColor": "#089282",
      "color": "#13564e"
    },
    "areasSettings": {
      "unlistedAreasColor": "#15A892",
      "outlineThickness": 0.1
    },
    "dataProvider": {
      "map": "worldLow",
      "images": images
    },
    "listeners": [{
      "event": "clickMapObject",
      "method": function( event ) { generateHTML(event.mapObject.title); }
    }],
    "export": {
      "enabled": false
    }
  });
}

function generateHTML(title) {
  // {
  //   "name": "CIF schedule, HSGameTime scoreboard: Friday, Nov. 11",
  //   "sentiment": 0.625212,
  //   "url": "http://www.bing.com/cr?IG=B125CAB1917F49ABB6EBC4795C7B55C4&CID=01777D26AC066CE42A5374EAAD376D90&rd=1&h=JjyzC1o4tkSic_1hOG7095ig-HbmqnOkv6KakZQOWUY&v=1&r=http%3a%2f%2fwww.pe.com%2farticles%2fscoreboard-818380--.html&p=DevEx,5035.1",
  //   "long": "-70.666667",
  //   "datePublished": "2016-11-12T00:54:00",
  //   "location": "Santiago",
  //   "lat": "-33.45",
  //   "description": "Ramos (Big Bear) 16:10.4. Heat 1 team results — 1. Dana Hills 48. Others: 2. Great Oak 78, 7. Santiago 158. Heat 1 individuals — 1. C. Arriaga (Walnut) 17:16.8. Others in top 20: 4. Jarvis (Chaparral) 17:57.4, 11. Griffiths (Great Oak) 18:20.4 ..."
  // }

  var article = article_map.get(title);

  var template =
  '<h1><a href=' + article.url + ' target="_blank">' + article.name + '</a></h1>' +
  '<h2>' + article.location + ', ' + new Date(article.datePublished) + '</h2>' +
  '<p>' + article.description + '</p>'

  $('#news-panel').html(template);
}

function showNewsPanel() {

}

function hideNewsPanel() {

}
