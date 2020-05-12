# start from an official image
FROM nginx:latest
LABEL net.juniper.vendor "Juniper Networks"
LABEL description "UFTS"
ARG UFTS_UID
ARG UFTS_GID

COPY group /etc/group
RUN groupmod -g "${UFTS_GID}" nginx && usermod -u "${UFTS_UID}" nginx
RUN chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid
EXPOSE 8080
USER nginx:nginx
