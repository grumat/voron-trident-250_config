# Automount Feature for External `.gcode` Files

## Create a mount point

Use `root` account:

```sh
mkdir -p /home/klipper/printer_data/gcodes/usb
chown klipper:klipper /home/klipper/printer_data/gcodes/usb
```

## Create a `systemd` Mount Service Template

This template will mount any USB block device (e.g., `/dev/sda1`) to `/home/klipper/usb`.

Create the file:

```sh
nano /etc/systemd/system/usb-mount@.service
```

Paste this:

```ini
[Unit]
Description=Mount USB drive %I
After=local-fs.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/mount -o uid=klipper,gid=klipper,fmask=0111,dmask=0000,sync /dev/%I /home/klipper/printer_data/gcodes/usb
ExecStop=/bin/sync
ExecStop=/bin/umount /home/klipper/printer_data/gcodes/usb

[Install]
WantedBy=multi-user.target
```

## Create a `udev` Rule to Trigger the Mount

Create the rule:

```sh
nano /etc/udev/rules.d/99-usb-mount.rules
```

Add:

```ini
ACTION=="add", SUBSYSTEM=="block", KERNEL=="sd[a-z][0-9]", \
    RUN+="/bin/systemctl start usb-mount@%k.service"

ACTION=="remove", SUBSYSTEM=="block", KERNEL=="sd[a-z][0-9]", \
    RUN+="/bin/systemctl stop usb-mount@%k.service"
```

Reload udev:

```sh
udevadm control --reload-rules
udevadm trigger
```

