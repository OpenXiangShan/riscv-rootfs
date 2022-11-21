#!/bin/ash

# Config IP address through DHCP
# udhcpc
# ifconfig eth0 172.28.2.10 netmask 255.255.255.0
# ip route add default via 172.28.2.1
ifconfig eth0 192.168.1.2 netmask 255.255.255.0

# Mount NFS
# mount -t nfs -o defaults,nolock 172.28.9.102:/home/user01/xs_nfs /mnt
# mount -t nfs -o defaults,nolock 172.28.11.119:/home/cxhpc/nanhu-nfs/nfs /mnt
mount -t nfs -o defaults,nolock 192.168.1.200:/home/user01/nanhu-nfs /mnt

# Boot on NFS
exec switch_root /mnt /sbin/init
