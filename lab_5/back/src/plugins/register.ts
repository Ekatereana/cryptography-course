import { FastifyPluginCallback, RouteShorthandOptions } from 'fastify';
import { UserSignUp } from '../types/user';
import { IAuthService } from '../services/authService';

export interface RegisterPluginOptions {
  authService: IAuthService;
}

const registerSchema: RouteShorthandOptions = {
  schema: {
    body: {
      type: 'object',
      required: ['username', 'email', 'fullName', 'password'],
      properties: {
        username: { type: 'string' },
        email: { type: 'string' },
        fullName: { type: 'string' },
        password: { type: 'string' },
      },
    },
  },
};

export const registerPlugin: FastifyPluginCallback<RegisterPluginOptions> = (fastify, options, done) => {
  fastify.post('/auth/register', registerSchema, async (request, response) => {
    const userData = request.body as UserSignUp;
    try {
      await options.authService.register(userData);
      response.code(204);
    } catch (err) {
      console.log('register error:');
      console.error(err);
      response.code(err.status || 500).send(err.errorMessage || err);
    }
  });

  done();
};
