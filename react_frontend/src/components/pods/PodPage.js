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
    this.state = {
      pod: {},
      players: [],
      packs: [],
      decks: [],
      packCards: [],
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
    if (JSON.stringify(this.props.players) != JSON.stringify(nextProps.players)) {
      this.setState({players: nextProps.players});
    }
    if (JSON.stringify(this.props.packs) != JSON.stringify(nextProps.packs)) {
      this.setState({packs: nextProps.packs});
    }
    if (JSON.stringify(this.props.decks) != JSON.stringify(nextProps.decks)) {
      this.setState({decks: nextProps.decks});
    }
    if (JSON.stringify(this.props.packCards) != JSON.stringify(nextProps.packCards)) {
      this.setState({packCards: nextProps.packCards});
    }
    if (this.props.pickNumber != nextProps.pickNumber) {
      this.setState({pickNumber: nextProps.pickNumber});
    }
  }

  changePickNumber(event) {
    this.setState({pickNumber: event.target.value});
    let players = collectPodPlayers(this.state, this.props, event.target.value);
    this.setState({players: players});
  }

  render() {
    return (
      <div>
        <div className="row">
          <div className="col-md-5">
            <h1>{this.state.pod.name}</h1>({this.state.pickNumber})
          </div>
          <div className="col-md-2">
            pack sets: {this.state.pod.pack_1_set}, {this.state.pod.pack_2_set}, {this.state.pod.pack_3_set}
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

const getPods = (state, props) => state.pods;
const getPodId = (state, props) => props.params.podId;
const getPod = (state, props) => state.pod || Object.assign({}, state.pods.find(pod => pod.id == props.params.podId));
const getPlayers = (state, props) => state.players;
const getPacks = (state, props) => state.packs;
const getDecks = (state, props) => state.decks;
const getPackCards = (state, props) => state.packCards;


function collectPodPlayers(state, props, pickNumber) {
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
  let pod = {name: '', pack_1_set: '', pack_2_set: '', pack_3_set: '', player_ids: []};
  let players = [];
  let pickNumber = state.pickNumber || 1;
  if (state.pods.length > 0) {
    pod = Object.assign({}, state.pods.find(pod => pod.id == ownProps.params.podId));
    players = collectPodPlayers(state, ownProps, pickNumber);
  }
  let props = {pod: pod, players: players, packs: state.packs, decks: state.decks, packCards: state.packCards, pickNumber: pickNumber};
  return props;
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(podActions, dispatch)
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(PodPage);
