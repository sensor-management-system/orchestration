FROM node:10.16.3-stretch
RUN mkdir /ssmfrontend
COPY . /ssmfrontend
WORKDIR /ssmfrontend
RUN npm install

ENTRYPOINT ["npm"]
CMD ["run", "dev", "--", "-H", "0.0.0.0", "-p", "80"]

