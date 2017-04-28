"use strict";

var UserArticles = React.createClass({

    getInitialState: function () {
        return {user_id: "", username: "", f_name: "", l_name: "", 
        password: "", email: "", phone: ""};
    },

    componentDidMount: function () {
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
            }));
    },


//     handleEditClick: function () {
//          bring up a modal for editing!!!!!
//     },


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

        var userProfile = (

        <div>
            <h1>     User Profile: { this.state.f_name } { this.state.l_name }</h1>
            <br />
            <h5>     Username: { this.state.username }</h5>
            <h5>     Password: { this.state.password }</h5>
            <h5>     Email: { this.state.email }</h5>
            <h5>     Phone: { this.state.phone }</h5> 
        </div>
        );

    return userProfile;
        
    },
    

});

var theUserId = $('#id').data('userId');


ReactDOM.render(
    <UserArticles userId={theUserId} />,
    document.getElementById('root')
    );
/* end-main */