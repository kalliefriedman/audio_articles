"use strict";


$(document).ready(function(){

    var deletetag = $(".delete-tag");


    $("#audio_controls").hide();

    // prevents default and makes call to read route, constructing URL, on click
    $("#submit_read_request").click(function(event){
        event.preventDefault();
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
        //make the AJAX request
       $.post("/tag-add-process.json", formData, function(results){
                                                console.log(results);
                                                $("#tags").append(results + " * ");
                                                } //end of callback function
        ); //end of AJAX request
    } //end of tagadd


    

    //attach event listener to tag delete buttons
    $(deletetag).on("submit", deleteTag);
    //this is the event handler for submitting the tag button delete forms
    function deleteTag(evt) {
        console.log("deletingtag");
        evt.preventDefault();
        // get the form values
        var thisForm = evt.currentTarget;
        var articleId = $(thisForm).find("input[name='article_id']").val();
        var tagID = $(thisForm).find("input[name='tag_id']").val();
        var formData = {"tag_id": tagID, article_id: articleId};
        //make the AJAX request
        $.post("/delete-tag", formData, removeTagFromDom); //fix this to display removed tag
         
        function removeTagFromDom(evt) {
            $( "form" ).remove( ":contains(name="tag_id" value=evt.tag_id));
        }

         //end of AJAX request
    } //end of deleteTag
}); //end of document.ready


// var SharkWords = React.createClass({

//     getInitialState: function () {
//         return {numWrong: 0, guessed: new Set()}
//     },

//     guessedWord: function () {  // "app_e" for "apple"
//         var word = "";

//         for (var ltr of this.props.answer)
//             word += this.state.guessed.has(ltr) ? ltr : "_";

//         return word;
//     },

//     handleGuess: function (evt) {
//         var letter = evt.target.value;
//         this.state.guessed.add(letter);
//         this.setState({guessed: this.state.guessed});

//         if (this.props.answer.indexOf(letter) === -1)
//             this.setState({'numWrong': this.state.numWrong + 1});
//     },

//     renderButtons: function () {
//         var buttons = [];

//         for (var ltr of "abcdefghijklmnopqrstuvwxyz")
//             buttons.push(
//                 <button key={ ltr } value={ ltr }
//                         disabled={ this.state.guessed.has(ltr) }
//                         onClick={ this.handleGuess }>
//                     { ltr }
//                 </button>)

//         return <div className="letters">{ buttons }</div>;
//     },

//     render: function () {
//         return (
//             <div className="sharkwords">
//                 <h1>Sharkwords!</h1>
//                 <img src={ "guess" + this.state.numWrong + ".png" }/>
//                 <p className="guessed">
//                     Wrong guesses: { this.state.numWrong }
//                 </p>
//                 <p className="word">{ this.guessedWord() }</p>

//                 { this.renderButtons() }
//             </div>
//         )
//     },
// });

// /* start-main */
// var word = randomWord();
// console.log("answer = " + word);

// ReactDOM.render(
//     <SharkWords answer={ word }/>,
//     document.getElementById('root'));
// /* end-main */