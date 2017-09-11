import React, {PropTypes} from 'react';

const PlayerList = ({players}) => {
  return (
    <div>
      <h3>Players</h3>
      <ul>
        {players.map(player =>
            <li key={player.id}>{player.name}</li>
          )}
      </ul>
    </div>
  );
};

PlayerList.propTypes = {
  players: PropTypes.array.isRequired
};

export default PlayerList;