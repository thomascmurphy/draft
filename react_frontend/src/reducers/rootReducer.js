import {combineReducers} from 'redux';
import cats from './catReducer';

const rootReducer = combineReducers({
  // short hand property names
  pods,
  players
})

export default rootReducer;
