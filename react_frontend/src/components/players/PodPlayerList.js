import React, {PropTypes} from 'react';
import DeckCardList from '../packs/DeckCardList';

const PodPlayerList = ({players}) => {
  return (
    <div>
      {players.map(player =>
        <div key={player.id}>
          <div className="row">
            <div className="col-xs-12">
              <h2>{player.name} ({player.email})</h2>
            </div>
          </div>
          <div className="row" key={player.id}>
            <div className="col-sm-5">
              <h4>Pack {player.pack.number}</h4>
              <DeckCardList deckCards={player.pack_cards} />
            </div>
            <div className="col-sm-2">
              <h4>Pick {player.pick.pick_number}</h4>
              <img className="img-responsive" src={player.pick.image_url} alt={player.pick.id}/>
            </div>
            <div className="col-sm-5">
              <h4>Player Deck</h4>
              <DeckCardList deckCards={player.deck_cards} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

PodPlayerList.propTypes = {
  players: PropTypes.array.isRequired
};

export default PodPlayerList;