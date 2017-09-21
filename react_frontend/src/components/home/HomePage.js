import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {Link} from 'react-router';
import * as playerActions from '../../actions/playerActions';
import * as podActions from '../../actions/podActions';
import EmailForm from '../players/EmailForm';
import PodForm from '../pods/PodForm';
import {browserHistory} from 'react-router';

class HomePage extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      email: '',
      saving: false,
      pod: {name: '', players: [], pack_1_set: '', pack_2_set: '', pack_3_set: ''}
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

  createPod(event) {
    event.preventDefault();
    this.setState({saving: true});
    this.props.actions.createPod(this.state.pod).then((response) => {
      browserHistory.push('/pods');
    });
  }

  updatePodState(event) {
    const field = event.target.name;
    const pod = this.state.pod;
    pod[field] = event.target.value;
    return this.setState({pod: pod});
  }

  render() {
    return (
      <div>
        <div className="jumbotron">
          <h1>Draft Academy</h1>
          <p>draft with friends.</p>
        </div>
        <div className="row">
          <div className="col-sm-6">
            <h1>Continue Draft</h1>
            <EmailForm
              email={this.state.email}
              onSave={this.filterPlayers}
              onChange={this.updateEmailState}
              saving={this.state.saving}/>
          </div>
          <div className="col-sm-6">
            <h1>Start New Draft</h1>
            <PodForm
              pod={this.state.pod}
              players={this.state.pod.players}
              sets={this.props.sets}
              onSave={this.createPod}
              onChange={this.updatePod}
              saving={this.state.saving}/>
          </div>
        </div>
      </div>
    );
  }
}

HomePage.propTypes = {
  email: PropTypes.string,
  actions: PropTypes.object.isRequired,
  sets: PropTypes.array.isRequired
};

function mapStateToProps(state, ownProps) {
  if (state.sets.length > 0) {
    return {
      sets: state.sets
    };
  } else {
    return {
      sets: []
    };
  }
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(playerActions, podActions, dispatch)
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(HomePage);


/** WEBPACK FOOTER **
 ** ./src/components/home/HomePage.js
 **/
