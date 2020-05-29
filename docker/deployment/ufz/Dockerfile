FROM nginx:alpine

ARG BUILD_DATE
ARG VCS_REF

LABEL maintainer="Martin Abbrent <martin.abbrent@ufz.de>" \
    org.opencontainers.image.title="Sensor management frontend" \
    org.opencontainers.image.authors=" \
      Marc Hanisch <marc.hanisch@gfz-potsdam.de>  \
      Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>  \
      Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>"  \
    org.opencontainers.image.revision=$VCS_REF \
    org.opencontainers.image.created=$BUILD_DATE

COPY ./dist/ /usr/share/nginx/html/rdm/svm
