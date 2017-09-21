import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import { createSelectorCreator, defaultMemoize } from 'reselect'
import isEqual from 'lodash.isequal'
//import { collectPodPlayers } from '../../selectors'
import * as podActions from '../../actions/podActions';
import PodPlayerList from '../players/PodPlayerList';
import PodForm from './PodForm';

class PodPage extends React.Component {
  constructor(props, context) {
    super(props, context);
    // this.state = {
    //   pod: this.props.pod,
    //   players: this.props.players,
    //   pickNumber: 1
    // };
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
    this.setState({pickNumber: event.target.value});
    let players = collectPodPlayers(this.state, this.props);
    this.setState({players: players});
    console.log(this.state);
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
            <PodPlayerList players={this.state.players} />
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

const getPickNumber = (state, props) => state.pickNumber;
const getPods = (state, props) => state.pods;
const getPodId = (state, props) => props.params.podId;
const getPod = (state, props) => Object.assign({}, state.pods.find(pod => pod.id == props.params.podId));
const getPlayers = (state, props) => state.players;
const getPacks = (state, props) => state.packs;
const getDecks = (state, props) => state.decks;
const getPackCards = (state, props) => state.packCards;


function collectPodPlayers(state, props) {
  let pickNumber = getPickNumber(state, props);
  let pod = getPod(state, props);
  let players = getPlayers(state, props);
  let packs = getPacks(state, props);
  let decks = getDecks(state, props);
  let packCards = getPackCards(state, props);

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
      return player;
    }
  });
  return selected.filter(el => el != undefined);
}


// create a "selector creator" that uses lodash.isEqual instead of ===
// const createDeepEqualSelector = createSelectorCreator(
//   defaultMemoize,
//   isEqual
// )
//
// const collectPodPlayers = createDeepEqualSelector(
//   [getPickNumber, getPodId, getPods, getPlayers, getPacks, getDecks, getPackCards],
//   (pickNumber, podId, pods, players, packs, decks, packCards) => {
//     console.log(pickNumber, podId, pods, players, packs, decks, packCards);
//     if (!pickNumber) {pickNumber = 1;}
//     let pod = Object.assign({}, pods.find(pod => pod.id == podId));
//     let selected = players.map(player => {
//       if (player.pod_id == pod.id) {
//         let playerDeck = Object.assign({}, decks.find(deck => deck.player_id == player.id));
//         let playerPick = Object.assign({}, packCards.find(packCard => packCard.deck_id == playerDeck.id && packCard.pick_number == pickNumber));
//         let playerPack = Object.assign({}, packs.find(pack => pack.id == playerPick.pack_id));
//         let playerPackCards = Object.assign([], packCards.filter(packCard => packCard.pack_id == playerPack.id && (!packCard.pick_number || packCard.pick_number > pickNumber)));
//         let playerDeckCards = Object.assign([], packCards.filter(packCard => packCard.deck_id == playerDeck.id && packCard.pick_number < pickNumber));
//         player['pick'] = playerPick;
//         player['pack'] = playerPack;
//         player['deck'] = playerDeck;
//         player['pack_cards'] = playerPackCards;
//         player['deck_cards'] = playerDeckCards;
//         return player;
//       }
//     });
//     return {pod: pod, players: selected.filter(el => el != undefined), pickNumber: pickNumber};
//   }
// );


function mapStateToProps(state, ownProps) {
  let pod = {name: '', pack_sets: '', player_ids: []};
  let players = [];
  let pickNumber = state.pickNumber || 1;
  if (state.pods.length > 0) {
    if (pod.player_ids.length > 0) {
      players = collectPodPlayers(state, ownProps);
    }
  }
  return {pod: pod, players: players, pickNumber: pickNumber};
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(podActions, dispatch)
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(PodPage);
