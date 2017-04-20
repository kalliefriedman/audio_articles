"use strict";

filters = $(".filter");

function getFilteredArticles(tagvalue) {
    $.get('/filter-articles/' + tagvalue, displayArticles);}

filters.on('click', function(evt) {
var tagvalue = $(this).data("tagname");
getFilteredArticles(tagvalue);
});

function displayArticles(articles_object) {
  $("#display-articles").empty();
  $("#display-articles").append("<br>");
  console.log("emptied");
  for (var key in articles_object) {
    let value = articles_object[key];
    $("#display-articles").append("<ul><li><a href=/article-closeup/"+key+">"+value+"</a></li></ul>");
  }
}