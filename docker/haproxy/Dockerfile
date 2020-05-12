FROM haproxy:latest
LABEL net.juniper.vendor "Juniper Networks"
LABEL description "UFTS"
RUN mkdir -p /etc/ssl/certs/
RUN groupadd -r haproxy && useradd --no-log-init -r -g haproxy haproxy
RUN mkdir -p /run/haproxy
RUN mkdir -p /var/lib/haproxy
RUN mkdir -p /var/run/