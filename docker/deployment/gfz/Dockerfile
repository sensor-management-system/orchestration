FROM node:10.16.3-stretch as js-builder

# First the urls for sms backend and cv backend
ARG SMS_BACKEND_URL_ARG
ENV SMS_BACKEND_URL $SMS_BACKEND_URL_ARG

ARG CV_BACKEND_URL_ARG
ENV CV_BACKEND_URL $CV_BACKEND_URL_ARG

# Then the client id for open id connect and the authority to contact
ARG CLIENT_ID_ARG
ENV NUXT_ENV_CLIENT_ID $CLIENT_ID_ARG

ARG AUTHORITY_ARG
ENV NUXT_ENV_AUTHORITY $AUTHORITY_ARG

# The redirect uris (those must be different per host on that the frontend runs)
ARG HOST_ARG
ENV NUXT_ENV_REDIRECT_URI http://${HOST}/login-callback
ENV NUXT_ENV_POST_LOGOUT_REDIRECT_URI http://${HOST}/logout-callback
ENV NUXT_ENV_SILENT_REDIRECT_URI http://${HOST}/silent-callback

# And those remaining settings
ENV NUXT_ENV_RESPONSE_TYPE id_token
# the following is the ufz setting
#ENV NUXT_ENV_SCOPE openid profile email
# and this is our setting
ENV NUXT_ENV_SCOPE profile
ENV NUXT_ENV_FILTER_PROTOCOL_CLAIMS false
ENV NUXT_ENV_AUTOMATIC_SILENT_RENEW true
# TODO; Check here if we still need this one
ENV NUXT_ENV_SILENT_RENEW_INTERVAL 6900000


RUN mkdir /ssmfrontend
COPY . /ssmfrontend
WORKDIR /ssmfrontend
RUN npm install
RUN npm run build

FROM nginx:alpine as webserver
COPY --from=js-builder /ssmfrontend/dist/ /usr/share/nginx/html
