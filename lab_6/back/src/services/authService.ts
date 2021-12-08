import { comparePasswords, hashPassword } from '../crypto/utils';
import { IUserRepository } from '../db/types';
import { AfterLogin, Credentials, User, UserSignUp } from '../types/user';
import { badCredentials } from './errors';
import * as uuid from 'uuid';
import { validateEmail, validateFullName, validatePassword, validateUsername } from '../utils/validation';

export interface IAuthService {
  login(credentials: Credentials): Promise<AfterLogin>;
  register(userData: UserSignUp): Promise<void>;
}

export class AuthService implements IAuthService {
  database: IUserRepository;

  constructor(database: IUserRepository) {
    this.database = database;
  }

  async login(credentials: Credentials): Promise<AfterLogin> {
    const user = await this.database.findUserByUsername(credentials.username);
    if (!user) {
      throw badCredentials();
    }
    if (user?.password && await comparePasswords(credentials.password, user?.password)) {
      return {
        id: user.id,
        fullName: user.fullName,
        email: user.email,
        username: user.username,
        sessionId: uuid.v4(),
      } as AfterLogin;
    }
    throw badCredentials();
  }

  async register(userData: UserSignUp): Promise<void> {
    await validateEmail(this.database, userData.email);
    await validateUsername(this.database, userData.username);
    validateFullName(userData.fullName);
    validatePassword(userData.password);

    const userId = uuid.v4();
    userData.password = await hashPassword(userData.password);

    const user: User = {
      ...userData,
      id: userId,
    };
    console.log(user);

    await this.database.saveUser(user);
  }
}
