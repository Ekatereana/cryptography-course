import { Pool, PoolClient, PoolConfig } from 'pg';
import { encryptParams } from '../crypto/utils';

export type QueryParamValue = number | string;
export type QueryParamWithOption = {
  isEncrypted: boolean,
  value: QueryParamValue
};
export type QueryParam = QueryParamValue | QueryParamWithOption;

export class PgClientWrapper {
  private client: PoolClient;

  constructor(client: PoolClient) {
    this.client = client;
  }

  public release() {
    this.client.release();
  }

  public async query(sqlQuery: string, params: QueryParam[]): Promise<any> {
    return this.client.query(sqlQuery, encryptParams(params));
  }
}

export class PgConnectionWrapper {
  private connectionPool: Pool;

  constructor(opts: PoolConfig) {
    try {
      this.connectionPool = new Pool(opts);
    } catch (e) {
      console.error('Failed to connect to Postgres: ', e);
      throw e;
    }
  }

  public async connect(): Promise<PgClientWrapper> {
    const client = await this.connectionPool.connect();
    return new PgClientWrapper(client);
  }
}
