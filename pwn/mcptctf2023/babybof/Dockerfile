FROM redpwn/jail

COPY --from=ubuntu:20.04 / /srv
COPY babybof /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 555 /srv/app/run
RUN chmod 444 /srv/app/flag.txt

ENV JAIL_MEM 20M
ENV JAIL_TIME 100
ENV JAIL_CONNS_PER_IP 1
