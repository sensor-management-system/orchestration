FROM node:10.16.3-stretch as js-builder
RUN mkdir /ssmfrontend
COPY . /ssmfrontend
WORKDIR /ssmfrontend
RUN npm install
RUN npm run generate

FROM nginx:stable-apline as webserver
COPY --from=js-builder /ssmfrontend/dist/ /usr/share/nginx/html
