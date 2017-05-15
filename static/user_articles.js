"use strict";

$(document).ready(function(){
var filters = $(".filter");

// hiding base template button since it's replicated in navbar
$("#logout-button").hide();

// making ajax request to filter articles route, passing in tagvalue from filter
function getFilteredArticles(tagvalue) {
    $.get('/filter-articles/' + tagvalue, displayArticles);}

// on click action, set data from filter equal to tagname and call getFilteredArticles
filters.on('click', function(evt) {
var tagValue = $(this).data("tagname");
console.log(tagValue);
getFilteredArticles(tagValue);
 });

// empying display-articles element before articles are appended to it
function displayArticles(articles_object) {
  $("#display-articles").empty();
  $("#display-articles").append("<br>");
  console.log("emptied");
  for (var key in articles_object) {
    var value = articles_object[key];
    $("#display-articles").append("<ul><li><a href=/article-closeup/"+key+">"+value+"</a></li></ul>");   }
 }
});