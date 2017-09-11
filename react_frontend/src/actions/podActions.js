import * as types from './actionTypes';
import podApi from '../api/podApi';

export function loadPods() {
  return function(dispatch) {
    return podApi.getAllPods().then(pods => {
      dispatch(loadPodsSuccess(pods));
    }).catch(error => {
      throw(error);
    });
  };
}

export function loadPodsSuccess(pods) {
  return {type: types.LOAD_PODS_SUCCESS, pods};
}

export function updatePod(pod) {
  return function (dispatch) {
    return podApi.updatePod(pod).then(responsePod => {
      dispatch(updatePodSuccess(responsePod));
    }).catch(error => {
      throw(error);
    });
  };
}

export function updatePodSuccess(pod) {
  return {type: types.UPDATE_POD_SUCCESS, pod};
}
