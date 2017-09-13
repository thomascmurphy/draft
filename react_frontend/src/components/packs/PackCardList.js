import React, {PropTypes} from 'react';
import { Link, IndexLink } from 'react-router';

class PackCardList extends React.Component {
  render() {var linkDisplay = {display: 'block', cursor: 'pointer'};
    return (
        <div className="row">
          {this.props.packCards.map(packCard =>
            <div className="col-sm-2" key={packCard.id}>
              <a style={linkDisplay} onClick={this.props.onClick}>
                <img className="img-responsive" src={packCard.image_url} alt={packCard.id}/>
              </a>
            </div>
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
