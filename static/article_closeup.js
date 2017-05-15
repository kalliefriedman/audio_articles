

"use strict";

$(document).ready(function(){

    var deletetag = $(".delete-tag");

// hiding buttons outlined on base template since they are being replicated on navbar
    $("#audio_controls").hide();
    $("#logout-button").hide();

// prevents default and makes call to read route, constructing URL, on click
    $("#submit_read_request").click(function(evt){
        evt.preventDefault();
        var voiceId = $("#voice-id").val();
        var articleText = $("#text").val();
        var articleId = $("#article-id").val();
        var src = "/read?text=" + articleText + "&article_id=" + articleId + "&voice=" + voiceId;
        $("#audio_controls").attr("src", src);
        $("#audio_controls").show(); 
    });



 //attach event listener to tag add form
    $("#add-tag-form").submit(doTagAdd);
    //show tag add modal
    $("#add-tags").click(function(evt) {
        $("#tag-field").val('');
        $("#add-tag-modal").modal("show");
    });

    //this is the event handler for submitting the tag add form
    function doTagAdd(evt) {
        evt.preventDefault();
        $("#add-tag-modal").modal("hide");
        //get the form values
        var tagValue = $("#tag-field").val();
        var articleId = $("#article-id").val();
        //pack up the form values into an object
        var formData = {"tag_value": tagValue, "article_id": articleId};
        console.log(formData);
        
        //make the AJAX request and append response to DOM in a form
       $.post("/tag-add-process.json", formData, function(results) {
                                                console.log(results);
                                                var tagId = results.tag_id;
                                                var articleId = results.article_id;
                                                var tagValue = results.tag_value;

                                                var newForm = $("<form>");
                                                newForm.attr("id", "tag-id-" + tagId);
                                                newForm.attr("class", "delete-tag");
                                                
                                                var articleIdInput = $("<input>");
                                                articleIdInput.attr("type", "hidden");
                                                articleIdInput.attr("name", "article_id");
                                                articleIdInput.attr("value", articleId);
                                                $(newForm).append(articleIdInput);

                                                var tagIdInput = $("<input>");
                                                tagIdInput.attr("type", "hidden");
                                                tagIdInput.attr("name", "tag_id");
                                                tagIdInput.attr("value", tagId);
                                                $(newForm).append(tagIdInput);

                                                var submitInput = $("<input>");
                                                submitInput.attr("class", "filter");
                                                submitInput.attr("type", "submit");
                                                submitInput.attr("name", "tag_value");
                                                submitInput.attr("value", tagValue + " x");
                                                $(newForm).append(submitInput);

                                                newForm.append(newForm);
                                                $("#tags").append(newForm);
                                                
                                                } //end of callback function
        ); //end of AJAX request
    } //end of tagadd
    

    //attach event listener to tag delete buttons
    $(deletetag).on("submit", deleteTag);
    //this is the event handler for submitting the tag button delete forms
    
    function deleteTag(evt) {
        if (confirm("Are you sure you want to delete this tag?")){
            console.log("deletingtag");
            evt.preventDefault();
            // get the form values
            var thisForm = evt.currentTarget;
            var articleId = $(thisForm).find("input[name='article_id']").val();
            var tagID = $(thisForm).find("input[name='tag_id']").val();
            var formData = {"tag_id": tagID, article_id: articleId};
        //make the AJAX request
            $.post("/delete-tag", formData, function(results) {
            console.log(results);
            $("#tag-id-"+ results.tag_id).remove();
            }
            );
        }
         //end of AJAX request
    } //end of deleteTag
}); //end of document.ready