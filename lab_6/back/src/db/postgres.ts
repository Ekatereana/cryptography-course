import { PoolConfig } from 'pg';
import { User } from '../types/user';
import { IUserRepository } from './types';
import { PgConnectionWrapper, QueryParamWithOption } from './pgWrapper';
import { decryptRow } from '../crypto/utils';

export class Postgres implements IUserRepository {
  private connectionPool: PgConnectionWrapper;

  constructor(opts: PoolConfig) {
    try {
      this.connectionPool = new PgConnectionWrapper(opts);
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
    )).rows.map((user: any) => {
      const decryptedUser = decryptRow(user, { 'full_name': true, username: true, email: true });
      return { ...decryptedUser, fullName: decryptedUser['full_name'], full_name: undefined }
    });
    client.release();
    return rows[0];
  }

  public async findUserByUsername(username: string): Promise<User | undefined> {
    const client = await this.connectionPool.connect();
    const rows = (await client.query(
        'select * from users where username = $1',
        [username],
    )).rows.map((user: any) => {
      const decryptedUser = decryptRow(user, { 'full_name': true, username: true, email: true });
      return { ...decryptedUser, fullName: decryptedUser['full_name'], full_name: undefined }
    });
    client.release();
    return rows[0];
  }

  public async findUserById(id: string): Promise<User | undefined> {
    const client = await this.connectionPool.connect();
    const rows = (await client.query(
        'select * from users where id = $1',
        [id],
    )).rows.map((user: any) => {
      const decryptedUser = decryptRow(user, { 'full_name': true, username: true, email: true });
      return { ...decryptedUser, fullName: decryptedUser['full_name'], full_name: undefined }
    });
    client.release();
    return rows[0];
  }

  public async saveUser(user: User): Promise<void> {
    const client = await this.connectionPool.connect();
    await client.query('insert into users values ($1, $2, $3, $4, $5)', [
      user.id,
      { value: user.username, isEncrypted: true },
      { value: user.email, isEncrypted: true },
      { value: user.fullName, isEncrypted: true },
      user.password as string,
    ]);
    client.release();
  }
}
