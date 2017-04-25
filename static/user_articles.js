"use strict";

$(document).ready(function(){
var filters = $(".filter");
$("#logout-button").hide();


function getFilteredArticles(tagvalue) {
    $.get('/filter-articles/' + tagvalue, displayArticles);}

filters.on('click', function(evt) {
var tagValue = $(this).data("tagname");
console.log(tagValue);
getFilteredArticles(tagValue);
 });

function displayArticles(articles_object) {
  $("#display-articles").empty();
  $("#display-articles").append("<br>");
  console.log("emptied");
  for (var key in articles_object) {
    var value = articles_object[key];
    $("#display-articles").append("<ul><li><a href=/article-closeup/"+key+">"+value+"</a></li></ul>");   }
 }
});