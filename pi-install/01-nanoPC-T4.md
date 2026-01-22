# NanoPC-T4

Tested Software Options:

## Debian Minimal

Official. Easy to install. Not really *compact*.

Follow this selection path here:  
![](images/debian.png)  
[One Drive &rarr; 01_Official images &rarr; 02_SD-t-eMMC Images &rarr; rk3399-eflasher-debian-trixie-core-4.19-arm64-20260112.img.gz](http://download.friendlyelec.com/NanoPC-T4)

## Armbian

Community Edition. Difficult to Install (needs Linux or official linux on SD card). Up to Date.
Boot still contains some quirks and unhandled minor hardware exceptions ignored.

![](https://docs.armbian.com/images/logo-small.png)

[Images can found here.](https://www.armbian.com/nanopc-t4/)

Note the following:
- **NanoPC-T4** is **Community Maintained**
- The website recommends as alternative **NanoPi M4 V2** which has **Standard Support**.


Both distribution are broken and didn't show `wlan0`.

## DietPi

Very Stable. Difficult to Install (needs Linux or official linux on SD card). Up to Date. Uses less disk space. Support for the **NanoPC-T4** specific hardware **is broken**. One USB2 port does not work and USB-C "host" device tree overload has no effect.
This was the chosen one.

![](https://dietpi.com/docs/assets/images/dietpi-logo_180x180.png)

[Can be found here.](https://dietpi.com/docs/hardware/)

# Selected OS

Community distros are quite troublesome, so we will stick with the Official image.
