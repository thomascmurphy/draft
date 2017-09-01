import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import * as podActions from '../../actions/podActions';
import PodList from './PodList';

class PodsPage extends React.Component {
  render() {
    const pods = this.props.pods;
    return (
      <div className="col-md-12">
        <h1>Pods</h1>
        <div className="col-md-4">
          <PodList pods={pods} />
        </div>
        <div className="col-md-8">
          {this.props.children}
        </div>
      </div>
    );
  }
}


PodsPage.propTypes = {
  pods: PropTypes.array.isRequired
};

function mapStateToProps(state, ownProps) {
  // state = {pods: [{id:1, name: "Maru"}, etc.]}
  return {
    pods: state.pods
  };
}

export default connect(mapStateToProps)(PodsPage);
