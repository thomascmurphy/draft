import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import * as podActions from '../../actions/podActions';
import PlayerList from '../players/PlayerList';
import PodForm from './PodForm';

class PodPage extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      isEditing: false,
      pod: this.props.pod,
      podPlayers: this.props.podPlayers,
      saving: false
    };
    this.updatePodState = this.updatePodState.bind(this);
    this.savePod = this.savePod.bind(this);
    this.toggleEdit = this.toggleEdit.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.pod.id != nextProps.pod.id) {
      this.setState({pod: nextProps.pod});
    }
  }

  toggleEdit() {
    this.setState({isEditing: !this.state.isEditing});
  }

  updatePodState(event) {
    const field = event.target.name;
    const pod = this.state.pod;
    pod[field] = event.target.value;
    return this.setState({pod: pod});
  }

  savePod(event) {
    event.preventDefault();
    this.setState({saving: true});
    this.props.actions.updatePod(this.state.pod);
  }


  render() {
    if (this.state.isEditing) {
    return (
      <div>
        <h1>edit pod</h1>
        <PodForm
          pod={this.state.pod}
          players={this.state.podPlayers}
          onSave={this.savePod}
          onChange={this.updatePodState}
          onPlayerChange={this.updatePodHobbies}
          saving={this.state.saving}/>
      </div>
      );
    }
    return (
      <div className="col-md-8 col-md-offset-2">
        <h1>{this.props.pod.name}</h1>
        <p>pack sets: {this.props.pod.pack_sets}</p>
        <PlayerList players={this.props.podPlayers} />
        <button onClick={this.toggleEdit}>edit</button>
      </div>
    );
  }
}

PodPage.propTypes = {
  pod: PropTypes.object.isRequired,
  podPlayers: PropTypes.array.isRequired,
  actions: PropTypes.object.isRequired
};

function collectPodPlayers(players, pod) {
  let selected = players.map(player => {
    if (pod.player_ids.filter(playerId => playerId == player.id).length > 0) {
      return player;
    }
  });
  return selected.filter(el => el != undefined);
}

function mapStateToProps(state, ownProps) {
  let pod = {name: '', pack_sets: '', player_ids: []};
  let podPlayers = [];
  const podId = ownProps.params.id;
  if (state.pods.length > 0) {
    pod = Object.assign({}, state.pods.find(pod => pod.id == podId));
    if (pod.player_ids.length > 0) {
      podPlayers = collectPodPlayers(state.players, pod);
    }
  }
  return {pod: pod, podPlayers: podPlayers};
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(podActions, dispatch)
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(PodPage);
