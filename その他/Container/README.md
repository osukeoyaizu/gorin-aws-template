## DockerfileのFROM
FROM <image>:<tag>

### 公式のリポジトリにあるイメージを使用する場合
- 保存場所:https://hub.docker.com/

- 例: FROM python:3.7-slim
    - https://hub.docker.com/layers/library/python/3.7-slim/images/sha256-165301af208e762f90a554a1bf5848ec1d5b12950ce1d29ca06e1438182f6d19



## マルチステージビルド
```
ARG APP_HOME=/home/node/node-app
# build stage
FROM node:18-alpine as build
WORKDIR ${APP_HOME}
COPY ./node-app  ${APP_HOME}
RUN npm run build

# deploy stage
FROM nginx:alpine
COPY --from=build ${APP_HOME}/build /usr/share/nginx/html
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
```