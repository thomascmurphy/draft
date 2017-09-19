import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import * as playerActions from '../../actions/playerActions';
import PackCardList from './PackCardList';
import DeckCardList from './DeckCardList';

class PackPage extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      pack: this.props.pack,
      packCards: this.props.packCards,
      deckCards: this.props.deckCards,
      hash: this.props.hash,
      saving: false
    };
    this.savePick = this.savePick.bind(this);
  }

  componentDidMount() {console.log('componentDidMount');
    this.props.actions.loadPackCards(this.state.hash);
    this.props.actions.loadDeckCards(this.state.hash);
    this.props.actions.preloadImages(this.state.hash);
  }

  componentWillReceiveProps(nextProps) {console.log('will receive props', this.props, nextProps);
    if (this.props.hash != nextProps.hash) {
      console.log('receiveprops: player', nextProps);
      this.setState({hash: nextProps.hash});
    }
    if (JSON.stringify(this.props.pack) != JSON.stringify(nextProps.pack)) {
      console.log('receiveprops: load pack', nextProps);
      this.setState({pack: nextProps.pack});
    }
    if (JSON.stringify(this.props.packCards) != JSON.stringify(nextProps.packCards)) {
      console.log('receiveprops: load pack cards', this.props.packCards, nextProps.packCards);
      this.setState({packCards: nextProps.packCards});
    }
    if (JSON.stringify(this.props.deckCards) != JSON.stringify(nextProps.deckCards)) {
      console.log('receiveprops: load deck cards', this.props.deckCards, nextProps.deckCards);
      this.setState({deckCards: nextProps.deckCards});
    }
  }

  savePick(event) {
    event.preventDefault();
    this.setState({saving: true});
    this.props.actions.makePick(event.currentTarget.getAttribute('data-value'));
  }


  render() {
    const packCards = this.props.packCards;
    const deckCards = this.props.deckCards;
    var pack_title = 'Your Pack';
    var pack_card_list = <p>Waiting for your next pack to be passed</p>;
    if (this.props.pack.number > 0) {
      pack_title = "Pack #" + this.props.pack.number;
      pack_card_list = <PackCardList packCards={packCards} onClick={this.savePick} />;
    }
    return (
      <div className="row">
        <div className="col-md-6">
          <h1>{pack_title}</h1>
          {pack_card_list}
        </div>
        <div className="col-md-6">
          <h1>Your Deck</h1>
          <DeckCardList deckCards={deckCards} />
        </div>
      </div>
    );
  }
}

PackPage.propTypes = {
  pack: PropTypes.object.isRequired,
  packCards: PropTypes.array.isRequired,
  deckCards: PropTypes.array.isRequired,
  hash: PropTypes.string.isRequired,
  actions: PropTypes.object.isRequired
};

function collectPackCards(packCards, pack) {
  let selected = packCards.map(packCard => {
    if (packCard.pack_id == pack.id && !packCard.deck_id) {
      return packCard;
    }
  });
  console.log('collect:', selected);
  return selected.filter(el => el != undefined);
}

function mapStateToProps(state, ownProps) {
  let pack = {set_code: '', number: 0, complete: false};
  let packCards = [];
  let deckCards = state.deckCards.length > 0 ? state.deckCards : [];
  const hash = ownProps.params.hash;
  console.log('state', state);
  if (state.packs.length > 0 && state.packCards.length > 0) {
    let packId = state.packCards[0].pack_id;
    pack = Object.assign({}, state.packs.find(pack => pack ? pack.id == packId : false));
    packCards = collectPackCards(state.packCards, pack);
  }
  return {pack: pack, packCards: packCards, deckCards: deckCards, hash: hash};
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(playerActions, dispatch)
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(PackPage);
