FROM node:lts-alpine3.13

COPY *.json ./
COPY yarn.lock ./
COPY src ./src

RUN yarn install && yarn build

EXPOSE 8080

CMD ["node", "build/index.js"]
