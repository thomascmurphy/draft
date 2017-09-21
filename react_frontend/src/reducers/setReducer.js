import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function setReducer(state = initialState.sets, action) {
  switch(action.type) {
    case types.LOAD_SETS_SUCCESS:
      return Object.assign([], state, action.sets);
    default:
      return state;
  }
}
