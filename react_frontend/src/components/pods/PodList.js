import React, {PropTypes} from 'react';
import { Link, IndexLink } from 'react-router';

const PodList = ({pods}) => {
  return (
      <ul className="list-group">
        {pods.map(pod =>
          <li className="list-group-item" key={pod.id}>
            <Link to={'/players/' + pod.player_hash + '/pack'}  activeClassName="active">{pod.name}</Link>
          </li>
        )}
      </ul>
  );
};

PodList.propTypes = {
  pods: PropTypes.array.isRequired
};

export default PodList;
