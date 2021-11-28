import { Pool, PoolConfig } from 'pg';
import { User } from '../types/user';
import { IUserRepository } from './types';

export class Postgres implements IUserRepository {
  private connectionPool: Pool;

  constructor(opts: PoolConfig) {
    try {
      this.connectionPool = new Pool(opts);
    } catch (e) {
      console.error('Failed to connect to Postgres: ', e);
      throw e;
    }
  }

  public async findUserByEmail(email: string): Promise<User | undefined> {
    const client = await this.connectionPool.connect();
    const rows = (await client.query(
        'select * from users where email = $1',
        [email],
    )).rows;
    client.release();
    return rows[0];
  }

  public async findUserByUsername(username: string): Promise<User | undefined> {
    const client = await this.connectionPool.connect();
    const rows = (await client.query(
        'select * from users where username = $1',
        [username],
    )).rows.map((user) => ({ ...user, fullName: user['full_name'], full_name: undefined }));
    client.release();
    return rows[0];
  }

  public async findUserById(id: string): Promise<User | undefined> {
    const client = await this.connectionPool.connect();
    const rows = (await client.query(
        'select * from users where id = $1',
        [id],
    )).rows;
    client.release();
    const rawUser = rows[0];
    return {
      id: rawUser.id,
      username: rawUser.username,
      email: rawUser.email,
      fullName: rawUser['full_name'],
    } as User;
  }

  public async saveUser(user: User): Promise<void> {
    const client = await this.connectionPool.connect();
    await client.query('insert into users values ($1, $2, $3, $4, $5)', [
      user.id,
      user.username,
      user.email,
      user.fullName,
      user.password,
    ]);
    client.release();
  }

  public async findUsersByGroupId(groupId: string): Promise<string[]> {
    const client = await this.connectionPool.connect();
    const ids = (await client.query(
        'select user_id from groups2users where group_id=$1',
        [groupId]
    )).rows.map(row => row['user_id']);
    client.release();
    return ids;
  }
}
