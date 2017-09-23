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
      pod: {
        name: '',
        pack_1_set: 'HOU',
        pack_2_set: 'HOU',
        pack_3_set: 'AKH',
        players: [{email: ''}, {email: ''}, {email: ''}, {email: ''}, {email: ''}, {email: ''}, {email: ''}, {email: ''}]
      }
    };
    this.updateEmailState = this.updateEmailState.bind(this);
    this.filterPlayers = this.filterPlayers.bind(this);
    this.createPod = this.createPod.bind(this);
    this.updatePodState = this.updatePodState.bind(this);
    this.updatePlayerState = this.updatePlayerState.bind(this);
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

  updatePlayerState(event) {
    const playerIndex = event.currentTarget.getAttribute('data-custom');
    const field = event.target.name;
    const pod = this.state.pod;
    pod.players[playerIndex][field] = event.target.value;
    return this.setState({pod: pod});
  }

  render() {
    return (
      <div>
        <div className="page-header">
          <h1>Draft Academy <small>Draft with friends and learn from their picks</small></h1>
        </div>
        <div className="row">
          <div className="col-sm-6">
            <div className="panel panel-default">
              <div className="panel-heading">
                <h3 className="panel-title">Continue Draft</h3>
              </div>
              <div className="panel-body">
                <EmailForm
                  email={this.state.email}
                  onSave={this.filterPlayers}
                  onChange={this.updateEmailState}
                  saving={this.state.saving}/>
              </div>
            </div>
          </div>

          <div className="col-sm-6">
            <div className="panel panel-default">
              <div className="panel-heading">
                <h3 className="panel-title">Start New Draft</h3>
              </div>
              <div className="panel-body">
                <PodForm
                  pod={this.state.pod}
                  players={this.state.players}
                  sets={this.props.sets}
                  onSave={this.createPod}
                  onChange={this.updatePodState}
                  onPlayerChange={this.updatePlayerState}
                  saving={this.state.saving}/>
              </div>
            </div>
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
    actions: bindActionCreators(Object.assign({}, playerActions, podActions), dispatch)
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(HomePage);


/** WEBPACK FOOTER **
 ** ./src/components/home/HomePage.js
 **/
