import { User } from '../types/user';

export interface IUserRepository {
  saveUser: (user: User) => Promise<void>;
  findUserByEmail: (email: string) => Promise<User | undefined>;
  findUserByUsername: (username: string) => Promise<User | undefined>;
  findUserById: (id: string) => Promise<User | undefined>;
}
