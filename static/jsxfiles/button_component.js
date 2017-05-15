// this has not yet been integrated, this is a component for user profile page

var React = require('react');

var buttonStyle = {
  margin: '10px 10px 10px 0'
};

var Button = React.createClass({
  render: function () {
    return (
      <button
        className="btn btn-default"
        style={buttonStyle}
        data = {this.props.label, this.props.user_id}
        onClick={this.props.handleClick}>{this.props.label}</button>
    );
  }
});

module.exports = Button;