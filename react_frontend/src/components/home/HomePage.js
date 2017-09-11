import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {Link} from 'react-router';
import * as podActions from '../../actions/podActions';
import EmailForm from '../pods/EmailForm';

class HomePage extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      email: this.props.email,
      saving: false
    };
    this.updateEmailState = this.updateEmailState.bind(this);
    this.filterPods = this.filterPods.bind(this);
  }

  updateEmailState(event) {
    const field = event.target.name;
    return this.setState({email: event.target.value});
  }

  filterPods(event) {
    event.preventDefault();
    this.setState({saving: true});
    this.props.actions.loadPods(this.state.email);
  }

  render() {
    return (
      <div>
        <div className="jumbotron">
          <h1>Draft Academy</h1>
          <p>draft with friends.</p>
        </div>
        <div>
          <h1>Contine Pod</h1>
          <EmailForm
            email={this.state.email}
            onSave={this.filterPods}
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
    actions: bindActionCreators(podActions, dispatch)
  };
}

export default connect(mapDispatchToProps)(HomePage);


/** WEBPACK FOOTER **
 ** ./src/components/home/HomePage.js
 **/