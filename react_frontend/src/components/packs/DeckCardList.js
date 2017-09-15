import React, {PropTypes} from 'react';
import { Link, IndexLink } from 'react-router';

class DeckCardList extends React.Component {
  render() {
    return (
        <div className="row">
          {this.props.deckCards.map(deckCard =>
            <div className="col-sm-2" key={deckCard.id}>
              <img className="img-responsive" src={deckCard.image_url} alt={deckCard.id}/>
            </div>
          )}
        </div>
    );
  }
};

DeckCardList.propTypes = {
  deckCards: PropTypes.array.isRequired
};

export default DeckCardList;
