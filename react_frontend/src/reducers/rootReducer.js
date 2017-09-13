import {combineReducers} from 'redux';
import pods from './podReducer';
import players from './playerReducer';
import packs from './packReducer';
import packCards from './packCardReducer';

const rootReducer = combineReducers({
  // short hand property names
  pods,
  players,
  packs,
  packCards
});

export default rootReducer;
