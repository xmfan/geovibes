var data;
var article_map = new Map();

$.get("http://10.8.86.139:5000/events", function(res) {
  articles_array = JSON.parse(res).response;
  generateMap(generateImages(articles_array));
});

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
    "projection": "winkel3",
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
    "export": {
      "enabled": true
    }
  });
}
