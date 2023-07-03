FROM node:gallium-bullseye AS deps
WORKDIR /home/node/app
COPY --chown=node:node package.json .
COPY --chown=node:node package-lock.json .
RUN npm install
RUN chown -R node:node node_modules/
COPY --chown=node:node . .
