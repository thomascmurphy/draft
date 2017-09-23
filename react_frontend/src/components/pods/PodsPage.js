import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import * as podActions from '../../actions/podActions';
import PodList from './PodList';

class PodsPage extends React.Component {
  render() {
    const pods = this.props.pods;
    return (
      <div className="row">
        <h1>Your Pods</h1>
        <div className="col-md-6">
          <PodList pods={pods} />
        </div>
        <div className="col-md-6">
          {this.props.children}
        </div>
      </div>
    );
  }
}


PodsPage.propTypes = {
  pods: PropTypes.array.isRequired,
  children: PropTypes.object
};

function mapStateToProps(state, ownProps) {
  if (state.pods && state.pods.length > 0) {
    return {
      pods: state.pods
    };
  } else {
    return {
      pods: [{id: '', name: '', packSets: [], playerIds: []}]
    }
  }
}

export default connect(mapStateToProps)(PodsPage);
