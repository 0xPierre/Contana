# Docker file for running the frontend in vite
FROM node:21-alpine3.18

WORKDIR /app

COPY package.json .
COPY . .

RUN yarn


EXPOSE 5173

CMD ["yarn", "dev"]