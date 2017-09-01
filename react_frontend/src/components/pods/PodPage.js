import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import * as podActions from '../../actions/podActions';

class PodPage extends React.Component {
  render() {
    return (
      <div className="col-md-8 col-md-offset-2">
        <h1>{this.props.pod.name}</h1>
        <p>pack sets: {this.props.pod.pack_sets}</p>
      </div>
    );
  }
}

PodPage.propTypes = {
  pod: PropTypes.object.isRequired,
};

function mapStateToProps(state, ownProps) {
  let pod = {name: '', pack_sets: '', player_ids: []};
  const podId = ownProps.params.id;
  if (state.pods.length > 0) {
    pod = Object.assign({}, state.pods.find(pod => pod.id == id)
  }
  return {pod: pod};
}

export default connect(mapStateToProps)(PodPage);
