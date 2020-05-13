#FROM node:current-slim
FROM node

COPY --chown=node:node . /home/node/
WORKDIR /home/node/
#RUN chown -R node:node /home/node/

#RUN apt-get update \
#    && DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install \
#    build-essential \
#    python3 \
#    && apt-get -y autoremove \
#    && apt-get -y autoclean \
#    && rm -rf /var/lib/apt


USER node


RUN npm install
