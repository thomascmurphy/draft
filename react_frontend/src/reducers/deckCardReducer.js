import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function deckCardReducer(state = initialState.deckCards, action) {
  switch(action.type) {
    case types.LOAD_DECK_CARDS_SUCCESS:
      return Object.assign([], state, action.deck_cards);
    default:
      return state;
  }
}
