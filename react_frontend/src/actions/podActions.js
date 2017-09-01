import * as types from './actionTypes';
import podApi from '../api/podApi';

export function loadPods() {
  return function(dispatch) {
    return Api.getAllPods().then(pods => {
      dispatch(loadPodsSuccess(pods));
    }).catch(error => {
      throw(error);
    });
  };
}

export function loadPodsSuccess(pods) {
  return {type: types.LOAD_PODS_SUCCESS, pods};
}
