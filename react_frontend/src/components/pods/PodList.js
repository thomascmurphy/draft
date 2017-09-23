import React, {PropTypes} from 'react';
import { Link, IndexLink } from 'react-router';

const PodList = ({pods}) => {
  return (
      <ul className="list-group">
        {pods.map(pod =>
          <Link to={'/players/' + pod.player_hash + '/pack'} key={pod.id} className={!pod.complete ? "list-group-item list-group-item-success" : "list-group-item"} activeClassName="active">{pod.name}<span className="badge">{pod.complete ? "Complete" : "Ongoing"}</span></Link>
        )}
      </ul>
  );
};

PodList.propTypes = {
  pods: PropTypes.array.isRequired
};

export default PodList;
