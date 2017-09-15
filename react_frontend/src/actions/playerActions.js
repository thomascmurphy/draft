import * as types from './actionTypes';
import playerApi from '../api/playerApi';

export function loadPlayersSuccess(players) {
  return {type: types.LOAD_PLAYERS_SUCCESS, players};
}

export function filterPodsSuccess(pods) {
  return {type: types.LOAD_PODS_SUCCESS, pods};
}

export function loadPackCardsSuccess(pack_cards) {
  return {type: types.LOAD_PACK_CARDS_SUCCESS, pack_cards};
}

export function loadDeckCardsSuccess(deck_cards) {
  return {type: types.LOAD_DECK_CARDS_SUCCESS, deck_cards};
}

export function filterPacksSuccess(packs) {
  return {type: types.LOAD_PACKS_SUCCESS, packs};
}

export function filterDecksSuccess(decks) {
  return {type: types.LOAD_DECKS_SUCCESS, decks};
}

export function loadPlayers(email) {
  return function(dispatch) {
    return playerApi.getPlayers(email).then(players => {
      dispatch(loadPlayersSuccess(players.players));
      dispatch(filterPodsSuccess(players.pods));
    }).catch(error => {
      throw(error);
    });
  };
}

export function loadPackCards(hash) {
  return function(dispatch) {
    return playerApi.getPack(hash).then(pack => {
      dispatch(loadPackCardsSuccess(pack.pack_cards));
      dispatch(filterPacksSuccess([pack.pack]));
    }).catch(error => {
      throw(error);
    });
  };
}

export function loadDeckCards(hash) {
  return function(dispatch) {
    return playerApi.getDeck(hash).then(deck => {
      dispatch(loadDeckCardsSuccess(deck.deck_cards));
      dispatch(filterDecksSuccess([deck.deck]));
    }).catch(error => {
      throw(error);
    });
  };
}

export function makePick(packCardId) {
  return function(dispatch) {
    return playerApi.makePick(packCardId).then(response => {
      dispatch(loadPackCardsSuccess(response.pack_cards));
      dispatch(loadDeckCardsSuccess(response.deck_cards));
      dispatch(filterPacksSuccess([response.pack]));
    }).catch(error => {
      throw(error);
    });
  };
}
