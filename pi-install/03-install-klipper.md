
# Install Klipper

Switch to `klipper` user:

```sh
su - klipper
```

## Installing Via `kiauh`

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
- 4) [Advanced]
  - 5) [Input Shaper] 
    - Install? **Y**


# Install `KAMP` Plugin (Optional)

This is the *Klipper Adaptive Meshing Purging*, which I use the Line Purge feature.  
Instruction can be found [here](https://github.com/kyleisah/Klipper-Adaptive-Meshing-Purging).

![](https://github.com/kyleisah/Klipper-Adaptive-Meshing-Purging/raw/main/Photos/Logo/KAMP-Logo.png)

If in `root` acount, switch to your `klipper` user account.
```sh
su - klipper
```

Install with:

```sh
cd ~
git clone https://github.com/kyleisah/Klipper-Adaptive-Meshing-Purging.git
ln -s ~/Klipper-Adaptive-Meshing-Purging/Configuration printer_data/config/KAMP
cp ~/Klipper-Adaptive-Meshing-Purging/Configuration/KAMP_Settings.cfg ~/printer_data/config/KAMP_Settings.cfg
```

## My Configuration

Edit `~/printer_data/config/KAMP_Settings.cfg` and uncomment `Line_Purge.cfg` and `Voron_Purge.cfg` lines. Optionally increase the value of `variable_purge_margin`:

```ini
...
#[include ./KAMP/Adaptive_Meshing.cfg]       # Include to enable adaptive meshing configuration.
[include ./KAMP/Line_Purge.cfg]             # Include to enable adaptive line purging configuration.
[include ./KAMP/Voron_Purge.cfg]            # Include to enable adaptive Voron logo purging configuration.
#[include ./KAMP/Smart_Park.cfg]             # Include to enable the Smart Park function, ...
...

# For the DragonBurner, which runs very close to the bed I also change this settings:
variable_purge_margin: 30
```


# Install `klipper_lcd_menu` Plugin (Optional)

This is a very nice LCD Menu, a *must have* for those using the 12864 with knob.  
Detailed documentation [here](https://github.com/dasburninator/klipper_lcd_menu).

![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWYvddY9yHVtxvX-IW4FzqHqW8zvpAbpGF4Q&s)

If in `root` acount, switch to your `klipper` user account.
```sh
su - klipper
```

Install with:

```sh
cd ~
git clone https://github.com/dasburninator/klipper_lcd_menu
ln -s ~/klipper_lcd_menu ~/printer_data/config/lcd_menu
cp ~/klipper_lcd_menu/lcd_menu_settings.cfg ~/printer_data/config/
```

## My Configuration

Because my printer model is a Trident I adjusted the following line in the `~/printer_data/config/lcd_menu_settings.cfg` file:

```ini
# Set Voron Serial Number here. Leave the leading whitespace.
variable_voron_serial: " Trident"
```

Please check the source code of this plugin. Most menus depends on macros that you have to provide yourself.  
The repository contains backups of my configuration.


# Install `klipper-motd` Plugin (Optional)

In the case you want *klipper personalized* **MoTD** messages when you log in using SSH.  
Detailed information can be found [here](https://github.com/tomaski/klipper-motd).

![](https://github.com/tomaski/klipper-motd/raw/main/readme-head.gif)

If in `root` acount, switch to your `klipper` user account.
```sh
su - klipper
```

Install with:

```sh
cd ~
git clone https://www.github.com/tomaski/klipper-motd.git
chmod +x ./klipper-motd/setup.sh
sudo ./klipper-motd/setup.sh --install
sudo motd-config
```

After installing I made some dirty patches on the `/etc/update-motd.d/10-klipper-motd` file.

Add a `BOND_IP` environment variable:
```sh
# get host information
ETH_IP=`/sbin/ip -br addr show | awk '$1 ~ /^[e]/ && $3 != "" {result = result $3 " " } END{ print result}'`
WLAN_IP=`/sbin/ip -br addr show | awk '$1 ~ /^[w]/ && $3 != "" {result = result $3 " " } END{ print result}'`
# Added by grumat
BOND_IP=`/sbin/ip -br addr show | awk '$1 ~ /^[b]/ && $3 != "" {result = result $3 " " } END{ print result}'`
...
```

Changes the cpu temp block to:
```sh
# cpu temp (patched by grumat)
if test -f /sys/class/thermal/thermal_zone0/temp; then
    CPU_TEMP=$(awk '{printf("%.1f",$1/1000)}' /sys/class/thermal/thermal_zone0/temp)
else
    CPU_TEMP=`/usr/bin/vcgencmd measure_temp | cut -c "6-9"`
fi
```

Added more code on how `HOST_IP` is computed:

```sh
if [ -n "$ETH_IP" ]; then
  HOST_IP+="$V${ETH_IP}$D(lan)"
fi

if [ -n "$WLAN_IP" ]; then
    if [ -n "$ETH_IP" ]; then
      HOST_IP+="$D and "
    fi
  HOST_IP+="$V${WLAN_IP}$D(wifi)"
fi

# Added by grumat
if [ -n "$BOND_IP" ]; then
  HOST_IP+="$V${BOND_IP}$D(bond)"
fi
```

These patches covers:
- Missing IP address
- Missing CPU temperature
