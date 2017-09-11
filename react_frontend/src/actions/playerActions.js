import * as types from './actionTypes';
import playerApi from '../api/playerApi';

export function loadPlayersSuccess(players) {
  return {type: types.LOAD_PLAYERS_SUCCESS, players};
}

export function loadPlayers() {
  return function(dispatch) {
    return playerApi.getAllPlayers().then(players => {
      dispatch(loadPlayersSuccess(players));
    }).catch(error => {
      throw(error);
    });
  };
}
