import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import * as podActions from '../../actions/podActions';
import PodPlayerList from '../players/PodPlayerList';
import PodForm from './PodForm';

class PodPage extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      pod: this.props.pod,
      players: this.props.players,
      pickNumber: 1
    };
    this.changePickNumber = this.changePickNumber.bind(this);
  }

  componentDidMount() {
    let podId = this.props.params.podId;
    this.props.actions.loadPod(podId);
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.pod.id != nextProps.pod.id) {
      this.setState({pod: nextProps.pod});
    }
  }

  changePickNumber(event) {
    this.props.dispatch({pickNumber: event.target.value});
  }

  render() {
    return (
      <div>
        <div className="row">
          <div className="col-md-5">
            <h1>{this.props.pod.name}</h1>({this.state.pickNumber})
          </div>
          <div className="col-md-2">
            pack sets: {this.props.pod.pack_sets}
          </div>
          <div className="col-md-5">
            <input type="range" name="pickNumber" onChange={this.changePickNumber} defaultValue={this.state.pickNumber} min="1" max="45" step="1"/>
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            <PodPlayerList players={this.props.players} />
          </div>
        </div>
      </div>
    );
  }
}

PodPage.propTypes = {
  pod: PropTypes.object.isRequired,
  players: PropTypes.array.isRequired,
  pickNumber: PropTypes.number.isRequired,
  actions: PropTypes.object.isRequired
};

function collectPodPlayers(pickNumber, pod, players, packs, decks, packCards) {
  let selected = players.map(player => {
    if (player.pod_id == pod.id) {
      let playerDeck = Object.assign({}, decks.find(deck => deck.player_id == player.id));
      let playerPick = Object.assign({}, packCards.find(packCard => packCard.deck_id == playerDeck.id && packCard.pick_number == pickNumber));
      let playerPack = Object.assign({}, packs.find(pack => pack.id == playerPick.pack_id));
      let playerPackCards = Object.assign([], packCards.filter(packCard => packCard.pack_id == playerPack.id && (!packCard.pick_number || packCard.pick_number > pickNumber)));
      let playerDeckCards = Object.assign([], packCards.filter(packCard => packCard.deck_id == playerDeck.id && packCard.pick_number < pickNumber));
      player['pick'] = playerPick;
      player['pack'] = playerPack;
      player['deck'] = playerDeck;
      player['pack_cards'] = playerPackCards;
      player['deck_cards'] = playerDeckCards;
      console.log(player);
      return player;
    }
  });
  return selected.filter(el => el != undefined);
}

function mapStateToProps(state, ownProps) {
  let pod = {name: '', pack_sets: '', player_ids: []};
  let players = [];
  let pickNumber = state.pickNumber || 2;
  const podId = ownProps.params.podId;
  if (state.pods.length > 0) {
    pod = Object.assign({}, state.pods.find(pod => pod.id == podId));
    if (pod.player_ids.length > 0) {
      players = collectPodPlayers(pickNumber, pod, state.players, state.packs, state.decks, state.packCards);
    }
  }
  return {pod: pod, players: players, pickNumber: pickNumber};
}

function mapDispatchToProps(dispatch) {
  const boundActionCreators = bindActionCreators(podActions, dispatch);
  const allActionProps = {...boundActionCreators, dispatch};
  return allActionProps;
}

export default connect(mapStateToProps, mapDispatchToProps)(PodPage);
