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

## Erase eMMC

THis is required to make sure that boot happens on the SD card. eMMC has priority.

- Download RkDevTool_v3.7 from official site.
- Insert USB-C cable
- Turn device on holding **Recovery** button
- If needed the FriendlyElec website has instruction and resources to install needed device drivers.
- Open **Advanced Function** Tab
- Press the `...` to choose the **Boot** file and select `.\rk3399\MiniLoaderAll.bin` file.
- Click the `Download` button to transfer.
- Click on `2. EMMC` on the list of devices
- Click on `EraseAll` button to clear the eMMC

**Warning:** Didn't find a way to flash a Linux image into the eMMC using this tool. It seems that an Android partition layout is required there.

