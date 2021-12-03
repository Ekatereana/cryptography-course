import { IUserRepository } from '../db/types';
import { User } from '../types/user';

export interface IUserService {
  findUserById(id: string): Promise<User>;
}

export class UserService implements IUserService {
  private userRepository: IUserRepository;

  constructor(userRepository: IUserRepository) {
    this.userRepository = userRepository;
  }

  public async findUserById(id: string): Promise<User> {
    const user = await this.userRepository.findUserById(id);
    if (user) {
      user.password = undefined;
      return user;
    } else {
      throw { status: 404, errorMessage: `User with id=${id} not found!` };
    }
  }
}
