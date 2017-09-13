import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function playerReducer(state = initialState.players, action) {
  switch(action.type) {
    case types.LOAD_PLAYERS_SUCCESS:
      return Object.assign([], state, action.players);
    default:
      return state;
  }
}
