FROM node:10.16.3-stretch as js-builder
ENV BACKEND_URL 'http://rz-vm64.gfz-potsdam.de:5000'
RUN mkdir /ssmfrontend
COPY . /ssmfrontend
WORKDIR /ssmfrontend
RUN npm install
RUN npm run generate

FROM nginx:alpine as webserver
COPY --from=js-builder /ssmfrontend/dist/ /usr/share/nginx/html
