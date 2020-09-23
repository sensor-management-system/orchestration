FROM node:10.16.3-stretch as js-builder
ARG SMS_BACKEND_URL_ARG
ARG CV_BACKEND_URL_ARG
ENV SMS_BACKEND_URL $SMS_BACKEND_URL_ARG
ENV CV_BACKEND_URL $CV_BACKEND_URL_ARG
RUN mkdir /ssmfrontend
COPY . /ssmfrontend
WORKDIR /ssmfrontend
RUN npm install
RUN npm run build

FROM nginx:alpine as webserver
COPY --from=js-builder /ssmfrontend/dist/ /usr/share/nginx/html
