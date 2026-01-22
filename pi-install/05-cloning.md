# Migration of Data (between two SBC's)

## Home Relative Paths

Check configuration files and make sure paths are relative to `$HOME` directory. Most problematic is `moonraker.conf`.  
**Warning:** `KIAUH` seem to use absolute path names.

For example, `moonraker.conf`:
```ini
[server]
host: 0.0.0.0
port: 7125
klippy_uds_address: ~/printer_data/comms/klippy.sock	# fixed here!!!
...
```


## Stop Klipper Services

Do it on both SBC's;

```sh
su - klipper
sudo systemctl stop klipper
sudo systemctl stop moonraker
```

> Fluidd doesn’t matter; it’s just static files.

## Copy Data

On the old SBC:

```sh
rsync -av ~/printer_data/config/ klipper@192.168.0.30:~/printer_data/config/
rsync -av ~/printer_data/database/ klipper@192.168.0.30:~/printer_data/database/
rsync -av ~/printer_data/gcodes/ klipper@192.168.0.30:~/printer_data/gcodes/
rsync -av ~/printer_data/logs/ klipper@192.168.0.30:~/printer_data/logs/
```

## Backup of Entire NanoPC-T4 Image

> **Warning:** Requires a Linux PC!

### Prerequisites

- Boot Linux
- Use USB-C cable to connect Linux Host and **NanoPC-T4**
- Enter Maskrom Mode (`RESET` + `BOOT` button like describe at the start of this article)


### Check for SBC Connection

```sh
$ rkdeveloptool ld
DevNo=1 Vid=0x2207 Pid=0x330c LocationID=...
```


### Install Boot Loader

```sh
$ rkdeveloptool db MiniLoaderAll.bin
Downloading bootloader succeeded.
```


### Dump the Full Image

First, identify eMMC size:

```sh
$ rkdeveloptool rfi
Flash Info:
        Manufacturer: SAMSUNG, value=00
        Flash Size: 14910 MB
        Flash Size: 30535680 Sectors
        Block Size: 512 KB
        Page Size: 2 KB
        ECC Bits: 0
        Access Time: 40
        Flash CS: Flash<0>
```

Then dump:

Total size: 30.535.680 * 512 = 15.634.268.160
```sh
$ rkdeveloptool rl 0x0 15634268160 my-klipper-start-image.img
Read LBA to file (100%)
```

and compress:

```sh
xz -T0 -9 my-klipper-start-image.img
```


## Using this Image for Crash Recovery

This also require Maskroom mode (see steps above for details):

```sh
xz -d my-klipper-start-image.img.xz
rkdeveloptool db MiniLoaderAll.bin
rkdeveloptool ef
rkdeveloptool wl 0x0 my-klipper-start-image.img
rkdeveloptool rd
```
