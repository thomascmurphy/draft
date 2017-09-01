import React, {PropTypes} from 'react';

const PodList = ({pods}) => {
  return (
      <ul className="list-group">
        {pods.map(pod =>
          <li className="list-group-item" key={pod.id}>
            {pod.name}
          </li>
        )}
      </ul>
  );
};

PodList.propTypes = {  
  pods: PropTypes.array.isRequired
};

export default PodList;
