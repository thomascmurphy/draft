import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function podReducer(state = initialState.pods, action) {
  switch(action.type) {
    case types.LOAD_PODS_SUCCESS:
      return action.pods;
    case types.UPDATE_POD_SUCCESS:
      return [
        ...state.filter(pod => pod.id !== action.pod.id),
        Object.assign({}, action.pod)
      ];
    case types.CREATE_POD_SUCCESS:
      return [
        ...state.filter(pod => pod.id !== action.pod.id),
        Object.assign({}, action.pod)
      ];
    default:
      return state;
  }
}
