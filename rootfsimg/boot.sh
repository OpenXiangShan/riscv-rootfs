#!/bin/ash

# Config IP address through DHCP
# udhcpc
ifconfig eth0 172.28.11.10 netmask 255.255.255.0
ip route add default via 172.28.11.1

# Mount NFS
# mount -t nfs -o defaults,nolock 172.28.9.102:/home/user01/xs_nfs /mnt
mount -t nfs -o defaults,nolock 172.28.11.119:/home/cxhpc/nanhu-nfs/nfs /mnt

# Boot on NFS
exec switch_root /mnt /sbin/init
