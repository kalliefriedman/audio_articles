import UserProfile from "./user_profile_react.jsx";

// gets user ID from the DOM by element id
var theUserId = $('#id').data('userId');

// rendering the user profile className 
ReactDOM.render(
    <UserProfile userId={theUserId} />,
    document.getElementById('root')
    );
/* end-main */