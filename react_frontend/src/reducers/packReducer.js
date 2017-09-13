import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function packReducer(state = initialState.packs, action) {
  switch(action.type) {
    case types.LOAD_PACKS_SUCCESS:
      return Object.assign([], state, action.packs);
    default:
      return state;
  }
}
