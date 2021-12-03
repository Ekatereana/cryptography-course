import { FastifyPluginCallback } from 'fastify';
import { IAuthService } from '../services/authService';
import { IUserService } from '../services/userService';

export interface UserPluginOptions {
  userService: IUserService;
  authService: IAuthService;
}

export const userPlugin: FastifyPluginCallback<UserPluginOptions> = async (fastify, options, done) => {
  fastify.get('/auth/user/:id', async (request, response) => {
    const { id } = request.params as { id: string };
    try {
      response.code(200).send(JSON.stringify(await options.userService.findUserById(id)));
    } catch (err) {
      console.error(err);
      response.code(err.status || 500).send(err.errorMessage || err);
    }
  });

  done();
};
