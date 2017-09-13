import React, {PropTypes} from 'react';
import { Link, IndexLink } from 'react-router';
import PackCardView from './PackCardView';

class PackCardList extends React.Component {
  render() {var linkDisplay = {display: 'block', cursor: 'pointer'};
    return (
        <div className="row">
          {this.props.packCards.map(packCard =>
            <PackCardView packCard={packCard} onClick={this.props.onClick}/>
          )}
        </div>
    );
  }
};

PackCardList.propTypes = {
  packCards: PropTypes.array.isRequired,
  onClick: PropTypes.func.isRequired
};

export default PackCardList;
