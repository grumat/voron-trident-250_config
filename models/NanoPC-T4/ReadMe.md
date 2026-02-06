# NanoPC-T4 Holder for Voron Printer

I found used FriendyELEC NanoPC-T4 boards at very good prices and since RK3399 was one of the most powerful beasts of its era. Comparably it is almost as good as a RPi5.  
This particular board, is a very complete set and features:
- 6 Core ARM CPU
- 4GB RAM
- Embedded 16 GB eMMC
- 1 x USB 3 port
- 1 x USB-C OTG port, reconfigurable as host USB
- 2 x USB 2 port
- WiFi, including antennas
- 12V very stable barrel power supply connector
- Just a bit bigger than standard RPi
- Possibility to use a big chipset heatsink and benefit from passive heating
- µSD card reader
- NVME PCIe 2080 slot
- RTC


## Bill Of Materials

| Quantity | Description | Usage / Reference |
|:--------:|:------------|:------|
| 1 | FriendyELEC NanoPC-T4 | RK3399-based Klipper controller (used board on eBay)
| 1 | USB Hub PCB | https://de.aliexpress.com/item/1005007937606123.html
| 6 | M2/6mm self tapping screws | Fix for NanoPC-T4 board / USB Hub top board
| 2 | M3/8mm self tapping screws or M2.6/8mm | USB Hub top board
| 4 | M3/8mm | Main body to DIN rail clip
| 1 | 12x3.6mm round silicone feet | USB Hub top board stay (LAN)
| 1 | 10x2mm round silicone feet | USB Hub top board stay (SD)

> USB hub is optional, but recommended if using USB for MCU's.

## Printed parts

Use Voron profile. Filament for DIN clip can't be brittle.

| Quantity | Description | File Name |
|:--------:|:------------|:----------|
| 2 | DIN rail clip | din-rail-bracket-heat-insert-version-625mm.step
| 1 | Main NanoPC-T4 PCB mount | NanoPC-Rail-Body.stl
| 1 | Mini USB Hub PCB | UsbPcbHub2-Body.stl

