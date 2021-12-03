import { all, put, takeEvery } from 'redux-saga/effects';
import {
  loginRoutine,
  registerRoutine,
  logoutRoutine,
  loadUserRoutine,
  loadUserPermissionsRoutine
} from './routines';
import { toastr } from 'react-redux-toastr';
import apiClient from '../../helpers/webApi.helper';

function* loadPermissions(action: any) {
  const data = action.payload;
  yield put(loadUserPermissionsRoutine.success(data));
}

function* login(action: any) {
  const { username, password, history } = action.payload;
  try {
    const res = yield apiClient.post({ endpoint: '/auth/login', body: { username, password } });
    const parsedData = yield res.json();
    yield put(loginRoutine.success({
      id: parsedData.id,
      fullName: parsedData.fullName,
      username: parsedData.username,
      email: parsedData.email,
      roles: [parsedData.role]
    }));
    history.push('/dashboard');
  } catch (error) {
    yield put(loginRoutine.failure());
    toastr.error(error?.message || error.toString(), '');
    console.log('Error with Login');
    console.log(error);
  }
}

function* register(action: any) {
  const resisterData = action.payload;
  try {
    yield apiClient.post({ endpoint: '/auth/register', body: resisterData });
    yield put(registerRoutine.success());
    toastr.success('All good. You can login now.', "");
  } catch (error) {
    yield put(registerRoutine.failure());
    toastr.error('Failed to register', error?.message || error.toString());
    console.log('Error with register');
    console.log(error);
  }
}

function* logout(action: any) {
  const history = action.payload;
  try {
    yield apiClient.get({ endpoint: '/auth/logout' });
    yield put(logoutRoutine.success());
    // authProvider.setToken(null);
    history.push('/login');
  } catch(error) {
    yield put(logoutRoutine.failure());
    console.log('Error with logout');
    console.log(error);
  }
}

function* loadUserData(action: any) {
  const history = action.payload;
  try {
    const res = yield apiClient.get({ endpoint: '/auth/user/all' });
    const parsedData = yield res.json();
    parsedData.roles = [];
    yield put(loadUserRoutine.success(parsedData));
  } catch(error) {
    yield put(loadUserRoutine.failure());
    console.log('Error with fetching user data');
    console.log(error);
    toastr.error('Failed to load user data:', error?.message || error.toString());
    history.push('/login');
  }
}

export default function* authSagas() {
  yield all([
    yield takeEvery(loginRoutine.TRIGGER, login),
    yield takeEvery(registerRoutine.TRIGGER, register),
    yield takeEvery(logoutRoutine.TRIGGER, logout),
    yield takeEvery(loadUserRoutine.TRIGGER, loadUserData),
    yield takeEvery(loadUserPermissionsRoutine.TRIGGER, loadPermissions),
  ]);
}
