import { combineReducers } from 'redux';
import { reducer as toastr } from 'react-redux-toastr';
import authReducer from './auth/reducer';

export default combineReducers({
  toastr,
  auth: authReducer,
});
