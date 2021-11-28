import fastify, { FastifyReply, FastifyRequest, HookHandlerDoneFunction } from 'fastify';
import cors from 'fastify-cors';
import { healthCheckPlugin } from '../plugins/healthCheck';
import fastifyCookie from 'fastify-cookie';
import { RouteGenericInterface } from 'fastify/types/route';
import { IncomingMessage, ServerResponse } from 'http';
import { Server } from 'http';
import { userPlugin } from '../plugins/user';
import { loginPlugin } from '../plugins/login';
import { registerPlugin } from '../plugins/register';
import { IUserService } from '../services/userService';
import { IAuthService } from '../services/authService';

const allowUnauthorized = new Set(['/', '/healthz', '/auth/health', '/auth/login', '/auth/register']);

const cookieHook = (
    request: FastifyRequest<RouteGenericInterface, Server, IncomingMessage>,
    reply: FastifyReply<Server, IncomingMessage, ServerResponse, RouteGenericInterface, unknown>,
    done: HookHandlerDoneFunction
) => {
  if (!allowUnauthorized.has(request.url) && !request.cookies['Session']) {
    reply.code(401).send('User is not authorized');
  } else {
    done();
  }
};

export const createFastifyServer = (userService: IUserService, authService: IAuthService) => {
  const server = fastify({});
  server.register(cors, {
    origin: (_origin, cb) => {
      cb(null, true);
    },
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    credentials: true,
  });
  server.register(fastifyCookie);
  server.register(healthCheckPlugin, {});
  server.register(userPlugin, { userService, authService });
  server.register(loginPlugin, { authService });
  server.register(registerPlugin, { authService });
  server.addHook('onRequest', cookieHook);
  return server;
};
