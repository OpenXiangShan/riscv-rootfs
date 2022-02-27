#!/bin/ash

# Config IP address through DHCP
udhcpc

# Mount NFS
mount -t nfs -o defaults,nolock 172.28.9.102:/home/user01/xs_nfs /mnt

# Boot on NFS
exec switch_root /mnt /sbin/init
