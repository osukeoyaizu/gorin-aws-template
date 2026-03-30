ARG APP_HOME=/home/node/oyaizu-app

# build stage
FROM node:18-alpine as build
WORKDIR ${APP_HOME}

COPY ./oyaizu-app  ${APP_HOME}
RUN npm run build

# deploy stage
FROM nginx:alpine
COPY --from=build ${APP_HOME}/build /usr/share/nginx/html

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]

