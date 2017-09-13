import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function packCardReducer(state = initialState.packCards, action) {
  switch(action.type) {
    case types.LOAD_PACK_CARDS_SUCCESS:
      return Object.assign([], state, action.pack_cards);
    default:
      return state;
  }
}
