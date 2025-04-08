#!/bin/busybox sh

set -e

echo "Init started with PID: $$"

if [ "$$" -ne 1 ]; then
  echo "Error: /init must be PID 1"
  exit 1
fi

/bin/busybox --install -s

mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev
mkdir -p /run
mount -t tmpfs tmpfs /run

mkdir /ram_root
mount -t tmpfs -o size=6G tmpfs /ram_root

echo "Move disk fs into memory"
mount /dev/vda /mnt 
cp -r /mnt/* /ram_root/
umount /mnt

echo "Chroot into disk fs in memory"

mount --bind /dev /ram_root/dev
mount -t sysfs sysfs /ram_root/sys
mount -t sysfs proc /ram_root/proc
mount -t tmpfs tmpfs /ram_root/run

chroot /ram_root /bin/bash
