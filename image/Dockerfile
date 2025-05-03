FROM alpine:latest

RUN apk --no-cache --update add plan9port socat

RUN mkdir /usr/lib/plan9/proc
RUN mkdir /usr/lib/plan9/dev
RUN mkdir /usr/lib/plan9/srv
RUN mkdir /usr/lib/plan9/tmp && chown 1777 /usr/lib/plan9/tmp

# Create flag
RUN echo "degro_example_wip_flag" > /flag.txt && chmod 444 /flag.txt && \
    chown root:root /flag.txt

# Copy essentials
RUN cp /usr/bin/env /usr/lib/plan9/bin/env
RUN cp /bin/pwd /usr/lib/plan9/bin/pwd
RUN cp /lib/ld-musl-x86_64.so.1 /usr/lib/plan9/lib/ld-musl-x86_64.so.1

RUN mkdir -p /usr/lib/plan9/usr/ghost
#RUN echo """ \
#/bin/9 rc -i \
#""" > /usr/lib/plan9/starter.sh && chmod +x /usr/lib/plan9/starter.sh

COPY START.sh /START.sh
RUN chmod +x /START.sh

EXPOSE 564

CMD ["/START.sh"]
