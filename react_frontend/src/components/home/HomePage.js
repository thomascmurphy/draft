import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {Link} from 'react-router';
import * as playerActions from '../../actions/playerActions';
import EmailForm from '../players/EmailForm';
import {browserHistory} from 'react-router';

class HomePage extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      email: '',
      saving: false
    };
    this.updateEmailState = this.updateEmailState.bind(this);
    this.filterPlayers = this.filterPlayers.bind(this);
  }

  updateEmailState(event) {
    const field = event.target.name;
    return this.setState({email: event.target.value});
  }

  filterPlayers(event) {
    event.preventDefault();
    this.setState({saving: true});
    this.props.actions.loadPlayers(this.state.email);
    browserHistory.push('/pods');
  }

  render() {
    return (
      <div>
        <div className="jumbotron">
          <h1>Draft Academy</h1>
          <p>draft with friends.</p>
        </div>
        <div>
          <h1>Continue Draft</h1>
          <EmailForm
            email={this.state.email}
            onSave={this.filterPlayers}
            onChange={this.updateEmailState}
            saving={this.state.saving}/>
        </div>
      </div>
    );
  }
}

HomePage.propTypes = {
  email: PropTypes.string,
  actions: PropTypes.object.isRequired
};

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(playerActions, dispatch)
  };
}

export default connect(null, mapDispatchToProps)(HomePage);


/** WEBPACK FOOTER **
 ** ./src/components/home/HomePage.js
 **/
