import {combineReducers} from 'redux';
import pods from './podReducer';
import players from './playerReducer';

const rootReducer = combineReducers({
  // short hand property names
  pods,
  players
});

export default rootReducer;
