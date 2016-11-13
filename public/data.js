var data;

$.get("http://10.8.86.139:5000/events", function(res) {
  data = JSON.parse(res);
});
