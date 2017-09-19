import * as types from './actionTypes';
import podApi from '../api/podApi';
import {loadPackCardsSuccess, loadPlayersSuccess, filterPacksSuccess, filterDecksSuccess} from './playerActions'

export function loadPods() {
  return function(dispatch) {
    return podApi.getAllPods().then(pods => {
      dispatch(loadPodsSuccess(pods));
    }).catch(error => {
      throw(error);
    });
  };
}

export function loadPod(podId) {
  return function(dispatch) {
    return podApi.getPod(podId).then(response => {
      dispatch(loadPodsSuccess([response.pod]));
      dispatch(loadPackCardsSuccess(response.pack_cards));
      dispatch(loadPlayersSuccess(response.players));
      dispatch(filterPacksSuccess(response.packs));
      dispatch(filterDecksSuccess(response.decks));
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
    return podApi.updatePod(pod).then(response => {
      dispatch(updatePodSuccess(response.pods));
    }).catch(error => {
      throw(error);
    });
  };
}

export function updatePodSuccess(pod) {
  return {type: types.UPDATE_POD_SUCCESS, pod};
}
