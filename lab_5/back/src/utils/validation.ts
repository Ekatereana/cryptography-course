import { IUserRepository } from '../db/types';
import {
  fieldNotSetError,
  emailInvalidFormatError,
  emailTooLongError,
  userAlreadyExistsError,
  usernameInvalidFormatError,
  usernameTooLongError,
  fullNameInvalidFormatError,
  passwordTooShortError, passwordNotValidError,
} from '../services/errors';

const emailRegularExpression = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
const usernameRegularExpression = /^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*$/;
const fullNameRegularExpression = /^[a-zA-Z]{2,}(?: [a-zA-Z]+){0,2}$/;

export const validateEmail = async (db: IUserRepository, email: string | undefined, maxEmailLength = 250) => {
  if (email === undefined) {
    throw fieldNotSetError('email');
  }

  if (email.length > maxEmailLength) {
    throw emailTooLongError(email, maxEmailLength);
  }
  if (!emailRegularExpression.test(email)) {
    throw emailInvalidFormatError(email);
  }
  const user = await db.findUserByEmail(email);
  if (user) {
    throw userAlreadyExistsError(email);
  }
};

export const validateUsername = async (
    db: IUserRepository,
    username: string | undefined, maxUsernameLength = 250
) => {
  if (username === undefined) {
    throw fieldNotSetError('username');
  }
  if (username.length > maxUsernameLength) {
    throw usernameTooLongError(username, maxUsernameLength);
  }
  if (!usernameRegularExpression.test(username)) {
    throw usernameInvalidFormatError(username);
  }

  const user = await db.findUserByUsername(username);
  if (user) {
    throw userAlreadyExistsError(username);
  }
};

export const validateFullName = (fullName: string | undefined) => {
  if (fullName == undefined) {
    throw fieldNotSetError('fullName');
  }
  if (!fullNameRegularExpression.test(fullName)) {
    throw fullNameInvalidFormatError(fullName);
  }
};

export const validatePassword = (password: string | undefined, minPasswordLength = 10) => {
  if (password === undefined) {
    throw fieldNotSetError('password');
  }
  let lower = false;
  let upper = false;
  let num = false;
  let special = false;

  for (let i = 0; i < password.length; i++) {
    const c = password.charCodeAt(i);
    if (c >= 65 && c <= 90) {
      upper = true;
    }
    if (c >= 97 && c <= 122) {
      lower = true;
    }
    if (c >= 48 && c <= 57) {
      num = true;
    }
    if ((c >= 33 && c <= 47) || (c >= 58 && c <= 64) || (c >= 91 && c <= 96) || (c >= 123 && c <= 126)) {
      special = true;
    }
  }

  if (password.length < minPasswordLength) {
    throw passwordTooShortError(password, minPasswordLength);
  }

  let errors = '';
  if (!upper) {
    errors += 'Need at least one uppercase.\n';
  }
  if (!lower) {
    errors += 'Need at least one lowercase.\n';
  }
  if (!num) {
    errors += 'Need at least one number.\n';
  }
  if (!special) {
    errors += 'Need at least one special character.\n';
  }
  if (errors !== '') {
    throw passwordNotValidError(password, errors);
  }
};
