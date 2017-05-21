// this has not yet been integrated, this is a component for user profile page

import React from "react";

var buttonStyle = {
  margin: '10px 10px 10px 0'
};

var Button = React.createClass({
  render: function () {
    return (
      <button
        className="btn btn-default"
        onClick={this.props.handleClick}>{this.props.label}
        </button>
    );
  }
});

export default Button;