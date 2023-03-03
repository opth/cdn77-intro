FROM debian:bullseye-slim

RUN apt update && apt install -y tzdata; \
    apt clean;

RUN mkdir /var/run/sshd; \
    apt install -y openssh-server iputils-ping python3 curl daemontools wget rsync python3-pip vim; \
    apt clean;

RUN echo "    UsePAM yes" >> /etc/ssh/ssh_config;

RUN { \
    echo '#!/bin/bash -eu'; \
    echo 'ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime'; \
    echo 'exec "$@"'; \
    } > /usr/local/bin/entry_point.sh; \
    chmod +x /usr/local/bin/entry_point.sh;

RUN mkdir -p /root/.ssh; 

ADD ansible.pub /root/.ssh/authorized_keys

RUN chmod go-rw /root/.ssh/authorized_keys; cat /root/.ssh/authorized_keys

ENV TZ Europe/Prague

ENV ROOT_PASSWORD root

EXPOSE 22

ENTRYPOINT ["entry_point.sh"]
CMD    ["/usr/sbin/sshd", "-D", "-e"]