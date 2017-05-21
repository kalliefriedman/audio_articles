"use strict";

import Button from "./button_component.jsx";

var UserProfile = React.createClass({

// creating all variables in state, setting them equal to empty data type
    getInitialState: function () {
        return {username: "", f_name: "", l_name: "", 
        password: "", email: "", phone: ""};
    },

// calls function to mount components (before inital render )
    componentWillMount: function () {
        this.getUserInfo();
    },

    getUserInfo: function () {
        // We could use jQuery here for our AJAX request, but it seems
        // silly to bring in all of jQuery just for one tiny part.
        // Therefore, we use the new built-into-JS "fetch" API for
        // AJAX requests. Not all browsers support this, so we have
        // a "polyfill" for it in index.html.
        var userID = this.props.userId;
        fetch("/user_info_profile.json?user_id="+ userID, {
            method: 'get'
            })
            .then(r => r.json())
            .then(j => this.setState({
                username: j.username,
                f_name: j.f_name,
                l_name: j.l_name,
                password: j.password,
                email: j.email,
                phone: j.phone
            })
            ) //closing second "then statement"
                            .catch((err) => console.log(err));

    }, //closes getUserInfo function


    handleClickEdit: function () {
    console.log("hit the handleClickEdit")
    },


//     handleEditSubmit: function () {
//             postComment: function (e) {
//         e.preventDefault();

//         }

//         fetch("/update_profile_info.json",
//             {body: comment, method: "POST"})
//             .then(r => r.json())
//             .then(j => this.setState({
//                 message: j.message,
//                 messageType: "success"
//             }));
//     },

    render: function () {

// creates user profile (dumb component) with states set from above
debugger;
        var userProfile = (
        <div className="container-fluid image-container"> 
            <div className="row">
              <div className="col-xs-12">
                <br />
                <br />
                <br />
              </div> 
            </div> 
  
            <div className="row">
            <div className="col-xs-8 col-xs-offset-2 profile-info-column">

                <div id="profiletext">
                    <h1>     User Profile: { this.state.f_name } { this.state.l_name }</h1>
                    <br />
                    <h5>     Username: { this.state.username }</h5>
                    <h5>     Password: { this.state.password }</h5>
                    <h5>     Email: { this.state.email }</h5>
                    <h5>     Phone: { this.state.phone }</h5> 
                </div>
                </div> 
                </div> 
                <Button label="Edit" handleClick={this.handleClickEdit.bind(this)}/>
            </div> 
        );

    return userProfile;
        
    },
    

});

export default UserProfile; 