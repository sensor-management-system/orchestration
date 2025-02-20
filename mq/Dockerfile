# SPDX-FileCopyrightText: 2024
# - Joost Hemmen <joost.hemmen@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2
ARG DEBIAN_IMAGE=stable-slim
FROM debian:${DEBIAN_IMAGE} AS build
ARG MOSQUITTO_VERSION
WORKDIR /build

# install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget git build-essential cmake \
    libssl-dev libcjson-dev libwebsockets-dev \
    golang-go

# download mosquitto-go-auth repo
RUN git clone https://github.com/iegomez/mosquitto-go-auth.git /build/mosquitto-go-auth

# download mosquitto repo, save in /repo
RUN wget http://mosquitto.org/files/source/mosquitto-${MOSQUITTO_VERSION}.tar.gz; \
    tar xzvf mosquitto-${MOSQUITTO_VERSION}.tar.gz

RUN cd mosquitto-${MOSQUITTO_VERSION}; \
    make CFLAGS="-Wall -O2 -I/build/lws/include" LDFLAGS="-L/build/lws/lib" WITH_WEBSOCKETS=no; \
    make install;

ENV CGO_ENABLED=1
ENV CGO_CFLAGS="-I/usr/local/include -fPIC"
ENV CGO_LDFLAGS="-shared -Wl,-unresolved-symbols=ignore-all"

RUN cd mosquitto-go-auth; \
    go build -buildmode=c-archive go-auth.go; \
    go build -buildmode=c-shared -o go-auth.so; \
    go build pw-gen/pw.go

FROM debian:${DEBIAN_IMAGE} AS final
ARG MOSQUITTO_VERSION

WORKDIR /mosquitto

# install runtime dependencies
RUN apt-get update && \
    apt-get install -y \
    libc-ares2 openssl uuid tini wget libssl-dev libcjson-dev libwebsockets-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/lib/mosquitto /var/log/mosquitto && \
    groupadd mosquitto && \
    useradd -s /sbin/nologin mosquitto -g mosquitto -d /var/lib/mosquitto && \
    chown -R mosquitto:mosquitto /var/log/mosquitto/ && \
    chown -R mosquitto:mosquitto /var/lib/mosquitto/

COPY --from=build /build/mosquitto-go-auth/pw /mosquitto/pw
COPY --from=build /build/mosquitto-go-auth/go-auth.so /mosquitto/go-auth.so
COPY --from=build /build/mosquitto-${MOSQUITTO_VERSION}/mosquitto.conf /mosquitto/mosquitto.conf
COPY --from=build /usr/local/sbin/mosquitto /usr/sbin/mosquitto
COPY --from=build /usr/local/bin/mosquitto_passwd /usr/bin/mosquitto_passwd
COPY --from=build /usr/local/bin/mosquitto_sub /usr/bin/mosquitto_sub
COPY --from=build /usr/local/bin/mosquitto_pub /usr/bin/mosquitto_pub
COPY --from=build /usr/local/bin/mosquitto_rr /usr/bin/mosquitto_rr
COPY --from=build /usr/local/lib/libmosquitto* /usr/local/lib/

RUN ldconfig;

EXPOSE 1883 8883

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD [ "/usr/sbin/mosquitto", "-c", "/etc/mosquitto/mosquitto.conf" ]