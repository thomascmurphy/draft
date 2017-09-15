import React, {PropTypes} from 'react';
import { Link, IndexLink } from 'react-router';

class PackCardView extends React.Component {
  render() {
    var linkDisplay = {display: 'block', cursor: 'pointer'};
    return (
      <div className="col-sm-4" key={this.props.packCard.id}>
        <a style={linkDisplay} onClick={this.props.onClick} data-value={this.props.packCard.id}>
          <img className="img-responsive" src={this.props.packCard.image_url} alt={this.props.packCard.id}/>
        </a>
      </div>
    );
  }
}

PackCardView.propTypes = {
  packCard: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired
};

export default PackCardView;
