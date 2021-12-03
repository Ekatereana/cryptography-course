import { FastifyPluginCallback } from 'fastify';

export const healthCheckPlugin: FastifyPluginCallback<Record<string, never>> = (fastify, options, done) => {
  fastify.get('/healthz', (request, response) => {
    response.code(200).send('ok');
  });

  fastify.get('/', (request, response) => {
    response.code(200).send('ok');
  });

  done();
};
