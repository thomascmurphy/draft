import * as types from './actionTypes';
import playerApi from '../api/playerApi';

export function loadPlayersSuccess(players) {
  return {type: types.LOAD_PLAYERS_SUCCESS, players};
}

export function filterPodsSuccess(pods) {
  return {type: types.LOAD_PODS_SUCCESS, pods};
}

export function loadPackCardsSuccess(pack_cards) {
  console.log('filter packcards:', pack_cards);
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
    return playerApi.getPlayers(email).then(response => {
      dispatch(loadPlayersSuccess(response.players));
      dispatch(filterPodsSuccess(response.pods));
      console.log('filter pods: ', response.pods)
    }).catch(error => {
      throw(error);
    });
  };
}

export function loadPackCards(hash) {
  return function(dispatch) {
    return playerApi.getPack(hash).then(response => {
      dispatch(loadPackCardsSuccess(response.pack_cards));
      dispatch(filterPacksSuccess([response.pack]));
    }).catch(error => {
      throw(error);
    });
  };
}

export function loadDeckCards(hash) {
  return function(dispatch) {
    return playerApi.getDeck(hash).then(response => {
      dispatch(loadDeckCardsSuccess(response.deck_cards));
      dispatch(filterDecksSuccess([response.deck]));
    }).catch(error => {
      throw(error);
    });
  };
}

export function makePick(packCardId) {console.log('start makepick:', packCardId);
  return function(dispatch) {
    return playerApi.makePick(packCardId).then(response => {
      console.log('finish makepick:', response);
      dispatch(loadPackCardsSuccess(response.pack_cards));
      dispatch(loadDeckCardsSuccess(response.deck_cards));
      dispatch(filterPacksSuccess([response.pack]));
    }).catch(error => {
      throw(error);
    });
  };
}

export function preloadImages(hash) {console.log('preload images');
  return function(dispatch) {
    return playerApi.getCardImages(hash).then(response => {
      let images = response.card_image_urls.map((card_image_url) => {
        let img=new Image();
        img.src=card_image_url;
      });
    }).catch(error => {
      throw(error);
    });
  };
}
