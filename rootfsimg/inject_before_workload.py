import guestfs
import argparse
import os
from pathlib import Path
g = guestfs.GuestFS()

executable_list = [("before_workload", "/usr/bin"),
                   ("run.sh", "/usr/bin"),
                   ("task0.sh", "/usr/bin"),
                   ("task1.sh", "/usr/bin")]
services_list = [("before_workload.service", "/etc/systemd/system")]
upload_list = executable_list + services_list

soft_link_list = [("before_workload.service", "/etc/systemd/system", "/etc/systemd/system/multi-user.target.wants")]

def launch_and_mount(image, filesystem, mount_point):
    g.add_drive_opts(image)
    g.launch()

    if not filesystem:
        filesystems = g.list_filesystems()
        print(f"Discover partitions: {filesystems}, using first partition")

        if filesystems:
            g.mount(filesystems[0][0], mount_point)
        else:
            print("Not found any partitions")

    else:
        g.mount(filesystem, mount_point)


# python inject_before_workload.py -i ./euler_mysql_hello.service.ext2 -o /etc/systemd/system/multi-user.target.wants/mysqld.service -p /nfs/home/jiaxiaoyu/workspace/libguestfs/upload
def main():
    parser = argparse.ArgumentParser(description="Use guestfish operate image file")

    parser.add_argument("-i", "--image", required=True, help="Specify the path to the image to be patched.")
    parser.add_argument("-m", "--mount-point", default="/", help="Specify the mount point, default is '/'")
    parser.add_argument("-f", "--file-system", default="/dev/sda", help="Specify the device to be mounted, default is '/dev/sda'")
    parser.add_argument("-o", "--workload-systemd-service", help="Specify the absolute path of the service to be executed after 'before_workload'")
    parser.add_argument("-p", "--upload-src", default="upload", help="Specify the directory containing files to be upload")
    parser.add_argument("--force-upload", action="store_true", default=False, help = "Upload files whatever exists")

    args = parser.parse_args()

    launch_and_mount(args.image, args.file_system, args.mount_point)

    for file in upload_list:
        if args.force_upload:
            g.upload(os.path.join(args.upload_src, file[0]), os.path.join(file[1], file[0]))
        try:
            g.ll(os.path.join(file[1], file[0]))
        except:
            g.upload(os.path.join(args.upload_src, file[0]), os.path.join(file[1], file[0]))

    for file in executable_list:
        g.chmod(0o755, os.path.join(os.path.join(file[1], file[0])))

    for file in soft_link_list:
        try:
            g.ll(os.path.join(file[2], file[0]))
        except:
            g.ln_s(os.path.join(file[1], file[0]), os.path.join(file[2], file[0]))
            print(g.ll(os.path.join(file[2], file[0])))

    if args.workload_systemd_service:
        g.download(args.workload_systemd_service, Path(args.workload_systemd_service).name)
        with open(Path(args.workload_systemd_service).name, 'r') as f:
            lines = f.readlines()

        new_lines = []
        inside_unit = False
        after_inserted = False

        for line in lines:
            new_lines.append(line)

            if line.strip() == "[Unit]":
                inside_unit = True
                continue

            if inside_unit and line.strip().startswith("After=") and not after_inserted:
                new_lines.append("After=before_workload.service\n")
                after_inserted = True

            if inside_unit and line.strip().startswith("[") and line.strip() != "[Unit]":
                inside_unit = False
        with open(Path(args.workload_systemd_service).name, "w") as f:
            f.writelines(new_lines)

        g.upload(Path(args.workload_systemd_service).name, args.workload_systemd_service)

    # check exists
    for file in upload_list:
        print(g.ll(os.path.join(file[1], file[0])))
    for file in soft_link_list:
        print(g.ll(os.path.join(file[2], file[0])))
    print(g.ll(args.workload_systemd_service))

    g.sync()
    g.umount(args.mount_point)
    g.close()


if __name__ == "__main__":
    main()
