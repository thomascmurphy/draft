import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function deckReducer(state = initialState.decks, action) {
  switch(action.type) {
    case types.LOAD_DECKS_SUCCESS:
      return Object.assign([], state, action.decks);
    default:
      return state;
  }
}
