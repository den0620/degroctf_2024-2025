#!/bin/sh

mount -t proc proc /usr/lib/plan9/proc
mount --bind /dev /usr/lib/plan9/dev

# Keep container running indefinitely
echo "Container started and running..."

export HOME=/usr/ghost
export PATH=/bin:/usr
export PLAN9=/

#socat TCP-LISTEN:564,fork,reuseaddr EXEC:"/usr/lib/plan9/bin/9 rc -i",chdir=/usr/lib/plan9,setuid=ghost,stderr
/usr/bin/socat TCP-LISTEN:3564,fork,reuseaddr EXEC:"/usr/sbin/chroot /usr/lib/plan9 /bin/rc -i",chdir=/usr/lib/plan9,stderr

