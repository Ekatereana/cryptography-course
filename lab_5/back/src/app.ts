import { Postgres } from './db/postgres';
import { IUserRepository } from './db/types';
import { IAuthService, AuthService } from './services/authService';
import { IUserService, UserService } from './services/userService';
import { checkAndGetEnv } from './utils/utils';
import { createFastifyServer } from './config/fastifyServer';

export class Application {
  private database: IUserRepository;
  private authService: IAuthService;
  private userService: IUserService;
  private fastifyServer: any;

  constructor() {
    checkAndGetEnv('CIPHER_KEY');
    this.database = new Postgres({
      max: 20,
      idleTimeoutMillis: 10000,
      connectionTimeoutMillis: 2000,
      connectionString: checkAndGetEnv('MAIN_DB_CONNECTION_STRING'),
    });
    this.authService = new AuthService(this.database);
    this.userService = new UserService(this.database);
    this.fastifyServer = createFastifyServer(this.userService, this.authService);
  }

  public startFastifyServer() {
    const port = checkAndGetEnv('HTTP_SERVER_PORT');
    this.fastifyServer.listen({ port }).then(() =>
      console.log(`App started! PORT: ${port}`),
    );
  }
}
