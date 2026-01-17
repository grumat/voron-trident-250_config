# OS Installation

Checked a series of options:

## Debian Minimal

Official. Easy to install. Seems to be frozen and generally outdated

## Armbian

Community Edition. Difficult to Install (needs Linux or official linux on SD card). Up to Date.
Boot still contains some quirks and unhandled minor hardware exceptions ignored.

## DietPi

Very Stable. Difficult to Install (needs Linux or official linux on SD card). Up to Date. Uses less disk space. Seems to have better support for this specific hardware.
THis was the chosen one.

# General Install Instructions

The easiest for is to have a Linux machine. I have Ubuntu, so my examples are taken from there.

## Prepare Ubuntu Linux machine

Apply updates:
```sh
sudo -i
apt update
apt upgrade
apt install -y rkdeveloptool usbutils
```

## Obtain the `MiniLoaderAll.bin` from Official FriendlyElec Site

A loader is required to work with low level tools. This file is called `MiniLoaderAll.bin` and is distributed with the RkDevTool (mine is v3.37) found on FriendlyElec site.

Copy the `MiniLoaderAll.bin` boot loader to Ubuntu home directory (`root` user plz). I use WinSCP for this.

## Copy the Image File

Since I chose DiatPi, I copied the `DietPi_NanoPCT4-ARMv8-Trixie.img` file into the root home directory, also using WinSCP.

## Connecting PC

Use an USB-C cable and connect to your Linux PC.

### Optional COM port

I also installed a USB/Serial TTL converter like the **CP2204** running on my Windows machine to monitor the SBC.  
The connection is at the side of the USB-C connector. Pin 1 begins at the side of the flat cable connector.
- **Pin 1:** GND
- **Pin 2:** Do not connect
- **Pin 3:** RX from the **CP2204**
- **Pin 4:** TX from the **CP2204**

Configure **Putty** or similar for the detected COM port using **1500000** as BAUD rate.


## Booting SBC in MaskRom Mode

Use these buttons:
- **`RESET` button:** Near the USB-C connector
- **`BOOT` button:** Between the `RECOVER` button and the 12V Fan connector

Procedure:
- Power SBC on
- Hold the `RESET` and the `BOOT` button at the same time. 
- Release `RESET` while holding `BOOT`
- Keep `BOOT` pressed for **5 seconds**, then release it.


## Check Connection

Type on Linux:

```sh
lsusb
```

Which approximately results:

```raw
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 26ce:01a2 ASRock LED Controller
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 003 Device 002: ID 0bda:5411 Realtek Semiconductor Corp. RTS5411 Hub
Bus 003 Device 003: ID 4348:7048 WinChipHead CH545
Bus 003 Device 004: ID 001f:0b21 Generic USB Audio
Bus 003 Device 005: ID 046a:0113 CHERRY KC 6000 Slim Keyboard
Bus 003 Device 006: ID 09da:3be3 A4Tech Co., Ltd. USB Device
Bus 003 Device 007: ID 1a86:e010 QinHeng Electronics HKS0401A3U
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 004 Device 002: ID 0bda:0411 Realtek Semiconductor Corp. Hub
Bus 005 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 005 Device 003: ID 2207:330c Fuzhou Rockchip Electronics Company RK3399 in Mask ROM mode
Bus 006 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
```

> Note that the SBC USB device (`ID 2207:330c`) is attached to the virtual machine.


## Check RK3399 Connection

Lets make sure you are using root account. Type 'sudo -i` if needed.

Check with:
```sh
$ rkdeveloptool ld
DevNo=1 Vid=0x2207,Pid=0x330c,LocationID=101    Maskrom
```

## Load Boot Loader


```sh
rkdeveloptool db MiniLoaderAll.bin
```

## Erase eMMC

```sh
rkdeveloptool ef
```

> This command is very fast and needs less than 10s to clear eMMC completely.

## Write Image

```sh
rkdeveloptool wl 0 DietPi_NanoPCT4-ARMv8-Trixie.img
```

> This command needs a couple of minutes, but it is considerably faster than the SD Card method.

## Reset the device

```sh
rkdeveloptool ef
```

If you are using the serial port, you can notice a classic Linux boot happening, which is done in more than one iteration.

Wait until you receive the login prompt.

If you are not using the serial port, you have to attach a keyboard/screen to your SBC to continue.

## Initial Configuration

Keep a LAN cable connected to help initial setup without the need of WiFi.

**Login:** root  
**Password:** dietpi

Wait for software installation and follow Wizard.
- Set new passwords
- **DietPi-Config** tool:
  - Performance Options:
    - CPU Governor: **performance**
  - Language/Regional Options:
    - Locale: **en_US.UTF-8**
	- Timezone: **Europe/Vienna**
	- Keyboard: **us**
  - Security Options:
	- Hostname: **Trident**
  - Network Options: 
    - Enable WiFi
	  - Scan and Configure SSID
	  - Set Country: **AT**
  - Software:
    - Browse Software:
      - 3: MC
	  - 17: Git
	  - 130: Python
    - SSH Server: **OpenSSH Server**
  - Press **Install** to apply changes


## Install SSH Keys

Install SSH Keys for better Putty WinSCP integration:

```sh
cd ~
mkdir .ssh			# only if not exists
chmod 0700 .ssh
cd .ssh
# Note replace by real valid keys
echo ssh-rsa AAAA...g4GwqAvMD6PRygl grumat-20220428 >> authorized_keys
echo ssh-rsa AAAA...PoT9AB9Lj/w== rsa-key-bjmm-20181215 >> authorized_keys
echo ssh-rsa AAAAAAABAAABA...5Pti1IMzSwh3Qt+c6JoR SW-X4 >> authorized_keys
chmod 0600 authorized_keys
```


## Combine Both Net Interfaces Into a Single IP Address

Since board supports both interfaces it is recommended to profit from an interesting feature. Use the following settings:

### Create the `/etc/network/interfaces.d/lan-wifi` File

This example uses the `192.168.0.20` IP address, which you should reserve on your router.

```ini
# Loopback
auto lo
iface lo inet loopback

# Ethernet (PRIMARY)
allow-hotplug eth0
iface eth0 inet static
    address 192.168.0.20
    netmask 255.255.255.0
    gateway 192.168.0.1
    dns-nameservers 1.1.1.1 8.8.8.8
    metric 100

# WiFi (FALLBACK)
allow-hotplug wlan0
iface wlan0 inet static
    address 192.168.0.20
    netmask 255.255.255.0
    gateway 192.168.0.1
    dns-nameservers 1.1.1.1 8.8.8.8
    metric 200
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
    pre-up iw dev wlan0 set power_save off
    post-down iw dev wlan0 set power_save on
```

> The `metric` value ensures LAN has lower priority over WiFi.

### Check the `/etc/wpa_supplicant/wpa_supplicant.conf` File

Ideally is to setup WiFi using `dietpi-config`, like suggested in the **Initial Configuration** topic above. 

Below follows a minimal reference, which highly depends on your WLAN router settings:

```ini
ctrl_interface=DIR=/run/wpa_supplicant GROUP=netdev
update_config=1
country=AT

network={
    ssid="MYROUTER"
    psk="your-wlan-password"
}
```

### Fix the `/etc/network/interfaces` File

Use your editor and remove interface contents and ensure this minimal contents:

```ini
source /etc/network/interfaces.d/*
```

### Reboot Your SBC

Reboot your SBC so that the new settings takes over. Now you should use the static address you selected before.

These are commands to check your settings:

```sh
ip addr show
ip route
```

Use your Windows host machine to ping the static address you chose.


## CANBUS Support

Add the `/etc/network/interfaces.d/can0` file to your system:

```ini
allow-hotplug can0
iface can0 can static
    bitrate 1000000
    up ip link set $IFACE txqueuelen 40
	pre-up ip link set can0 type can bitrate 1000000
	pre-up ip link set can0 txqueuelen 40

	post-up tc qdisc replace dev can0 root fq_codel
	post-down tc qdisc del dev can0 root || true
```

> Note tat Klipper docs recommend a `txqueuelen` of `128` bytes. Some statistical testing demonstrates a subtle improvement in timeout errors during probe calibration (on an umbilical system, this is a scenario that uses two controllers: one reading the probe and the other controlling stepper).

Check https://canbus.esoterical.online/mainboard_flashing for lots of CANBUS information.


## Other Packages

Always using root, install:

```sh
apt install build-essential
apt install python3-numpy python3-matplotlib libatlas3-base libopenblas-dev
```

## Create the `klipper` user

```sh
adduser klipper
```

- You’ll be prompted for a password
- You can leave the extra fields blank

This creates:

- `/home/klipper`
- A normal (non-root) user

### Grant sudo privileges (recommended way)

DietPi uses the standard Debian `sudo` setup.

Add the user to the `sudo` group:

```sh
sudo usermod -aG sudo klipper
```

### (Optional but recommended) Allow passwordless sudo for Klipper

Klipper scripts often assume non-interactive sudo.

Create a dedicated sudoers drop-in:

```sh
sudo visudo -f /etc/sudoers.d/klipper
```

Add **exactly** this line:

```ini
klipper ALL=(ALL) NOPASSWD:ALL
```

### Extra: serial/USB access (you’ll likely need this)

Klipper usually needs access to USB serial devices.

Add the user to required groups:

```sh
usermod -aG dialout,tty,video,input klipper
newgrp dialout
```

### Copy SSH keys for easy Login

Copy the keys used for `root` also for the `klipper` user.

```sh
cp ~/.ssh/authorized_keys /home/klipper/.ssh/
chown klipper:klipper /home/klipper/.ssh/authorized_keys
```

## Install Klipper

Switch to `klipper` user:

```sh
su - klipper
```

### Installing Via `kiauh`

> This needs `git`, which was installed on the **Initial Configuration** step.

```sh
cd ~ && git clone https://github.com/dw-0/kiauh.git
./kiauh/kiauh.sh
```

Follow these menu/steps:
- 1) [Install]
  - 1) [Klipper]
    - Number of instances: **1**
	- Create example.cfg: **Yes**
  - 2) [Moonraker]
    - Create moonraker.conf: **Yes**
  - 4) [Fluidd]
    - Download recommended Fluidd-Config: **Yes**
	- Port: **80**

