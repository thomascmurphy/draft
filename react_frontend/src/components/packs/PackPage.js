import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import * as playerActions from '../../actions/playerActions';
import PackCardList from './PackCardList';

class PackPage extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      pack: this.props.pack,
      packCards: this.props.packCards,
      hash: this.props.hash,
      saving: false
    };
    this.savePick = this.savePick.bind(this);
  }

  componentDidMount() {
    this.props.actions.loadPackCards(this.state.hash);
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.pack.id != nextProps.pack.id) {
      this.setState({pack: nextProps.pack});
    }
    if (this.props.packCards != nextProps.packCards) {
      this.setState({packCards: nextProps.packCards});
    }
  }

  savePick(event) {
    event.preventDefault();
    this.setState({saving: true});
    this.props.actions.makePick(event.target.value);
  }


  render() {
    const packCards = this.props.packCards;
    return (
      <div className="col-md-12">
        <h1>Pack #{this.props.pack.number}</h1>
        <PackCardList packCards={packCards} onClick={this.savePick} />
      </div>
    );
  }
}

PackPage.propTypes = {
  pack: PropTypes.object.isRequired,
  packCards: PropTypes.array.isRequired,
  hash: PropTypes.string.isRequired,
  actions: PropTypes.object.isRequired
};

function collectPackCards(packCards, pack) {
  let selected = packCards.map(packCard => {
    if (packCard.pack_id == pack.id && !packCard.deck_id) {
      return packCard;
    }
  });
  return selected.filter(el => el != undefined);
}

function mapStateToProps(state, ownProps) {
  let pack = {set_code: '', number: 0, complete: false};
  let packCards = [];
  const hash = ownProps.params.hash;
  if (state.packs.length > 0 && state.packCards.length > 0) {
    let packId = state.packCards[0].pack_id
    pack = Object.assign({}, state.packs.find(pack => pack.id == packId));
    packCards = collectPackCards(state.packCards, pack);
  }
  return {pack: pack, packCards: packCards, hash: hash};
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(playerActions, dispatch)
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(PackPage);
