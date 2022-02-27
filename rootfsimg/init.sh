#!/bin/busybox sh

/bin/busybox mount -t proc proc /proc
/bin/busybox mount -t sysfs sysfs /sys
/bin/busybox mount -t tmpfs tmpfs /tmp
/bin/busybox mount -o remount,rw /dev/htifbd0 /
/bin/busybox /bin/busybox --install -s
/bin/mkdir -p /dev/pts
/bin/echo /bin/mdev > /proc/sys/kernel/hotplug
/sbin/mdev -s

exec /bin/ash /boot.sh
