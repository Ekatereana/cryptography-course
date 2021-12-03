import { ApiError } from '../types/error';

export const fieldNotSetError = (field: string): ApiError => ({
  status: 400,
  errorCode: 'MISSING_FIELD',
  errorMessage: `Field ${field} must be set`,
});

export const emailInvalidFormatError = (_email: string): ApiError => ({
  status: 400,
  errorCode: 'EMAIL_INVALID',
  errorMessage: 'Invalid email',
});

export const usernameInvalidFormatError = (_email: string): ApiError => ({
  status: 400,
  errorCode: 'USERNAME_INVALID',
  errorMessage: 'Invalid username',
});

export const fullNameInvalidFormatError = (_fullName: string): ApiError => ({
  status: 400,
  errorCode: 'FULLNAME_INVALID',
  errorMessage: 'Invalid full name',
});

export const emailTooLongError = (_email: string, maxEmailLength: number): ApiError => ({
  status: 400,
  errorCode: 'EMAIL_TOO_LONG',
  errorMessage: `Email is too long: should not be longer than ${maxEmailLength} characters`,
});

export const usernameTooLongError = (_username: string, maxUsernameLength: number): ApiError => ({
  status: 400,
  errorCode: 'USERNAME_TOO_LONG',
  errorMessage: `Username is too long: should not be longer than ${maxUsernameLength} characters`,
});

export const passwordTooShortError = (_password: string, minPasswordLength: number): ApiError => ({
  status: 400,
  errorCode: 'PASSWORD_TOO_SHORT',
  errorMessage: `Password is too short: should be at least ${minPasswordLength} characters long`,
});

export const passwordNotValidError = (_password: string, message: string): ApiError => ({
  status: 400,
  errorCode: 'PASSWORD_NOT_VALID',
  errorMessage: `Password is not valid: ${message}`,
});

export const userAlreadyExistsError = (email: string): ApiError => ({
  status: 400,
  errorCode: 'USER_ALREADY_EXISTS',
  errorMessage: `User "${email}" already exists`,
});

export const badCredentials = (): ApiError => ({
  status: 400,
  errorCode: 'BAD_CREDENTIALS',
  errorMessage: 'Wrong username or password',
});
