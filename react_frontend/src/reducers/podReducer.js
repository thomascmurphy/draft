import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function podReducer(state = initialState.pods, action) {
  switch(action.type) {
    case types.LOAD_PODS_SUCCESS:
      return action.pods
    default:
      return state;
  }
}
