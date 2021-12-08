import { FastifyPluginCallback, RouteShorthandOptions } from 'fastify';
import { Credentials } from '../types/user';
import { IAuthService } from '../services/authService';

export interface LoginPluginOptions {
  authService: IAuthService;
}

const loginSchema: RouteShorthandOptions = {
  schema: {
    body: {
      type: 'object',
      required: ['username', 'password'],
      properties: {
        username: { type: 'string' },
        password: { type: 'string' },
      },
    },
  },
};

export const loginPlugin: FastifyPluginCallback<LoginPluginOptions> = async (fastify, options, done) => {
  fastify.post('/auth/login', loginSchema, async (request, response) => {
    const credentials = request.body as Credentials;
    try {
      const afterLoginDto = await options.authService.login(credentials);
      // 7 200 000 === 2 hours
      const expires = new Date();
      expires.setDate(expires.getTime() + 7200000);
      response.setCookie('Session', afterLoginDto.sessionId || '', {
        httpOnly: true,
        path: '/',
        secure: true,
        sameSite: 'none',
        domain: '127.0.0.1:8080',
        // expires,
      });
      response.code(200).send(JSON.stringify(afterLoginDto));
    } catch (err) {
      console.error(err);
      response.code(err.status || 500).send(err.errorMessage || err);
    }
  });

  done();
};
