FROM alpine:latest

RUN apk --no-cache --update add plan9port socat

RUN mkdir /usr/lib/plan9/proc
RUN mkdir /usr/lib/plan9/dev
RUN mkdir /usr/lib/plan9/srv
RUN mkdir /usr/lib/plan9/tmp && chown 1777 /usr/lib/plan9/tmp

# Create flag
RUN echo "degro_th3y_st1ll_avoid_plan9" > /flag.txt && chmod 444 /flag.txt && \
    chown root:root /flag.txt

# Copy essentials
RUN cp /usr/bin/env /usr/lib/plan9/bin/env
RUN cp /bin/pwd /usr/lib/plan9/bin/pwd
RUN cp /lib/ld-musl-x86_64.so.1 /usr/lib/plan9/lib/ld-musl-x86_64.so.1

RUN mkdir -p /usr/lib/plan9/usr/ghost
RUN echo "Тебе нужно покинуть это место" > /usr/lib/plan9/usr/ghost/NOTE.txt

COPY START.sh /START.sh
RUN chmod +x /START.sh

EXPOSE 3564

CMD ["/START.sh"]
