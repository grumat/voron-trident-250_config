# Heat Soaking Test

These charts shows a stress test for different Z-Probes. The test consists in running PROBE_ACCURACY continuously and store all samples, during the se 4 phases:
- **Phase 1:** Cold state (5 minutes)
- **Phase 2:** Heating bed and hot-end until they reach work temperature (variable duration)
- **Phase 3:** Heat soaking (30 minutes)
- **Phase 4:** Cool down (5 minutes)


# Charts

The black line is the Z value, which the absolute value is meaningless, since this is the difference of the Z-endstop switch and the Z calibration. This element is usually calibrated using screws and no single mount is comparable. But difference along the use is important.

The blue line shows the temperature of the head bed, which tends to shift the Z-Probe readings because of thermal expansion. The behavior of the Z curve shows how fine a temperature compensation compensation circuit is.

The red line shows temperature for the hot end, which is usually very near to the Z-probe and also influences Z readings, similar to the heat bed.

The graph scale marking shows `Z10+ diff` and `Z10+ stddev` values, simulating a heat soak of 10 minutes on the red area.


## SuperPinda (Prusa / Pepperl&Fuchs)

![](data/probe_accuracy_superpinda.jpg)

### Info

- Price: €26.00
- Web: https://www.prusa3d.com/product/superpinda/
- Minimum Heat soaking time: 3 minutes

### Pros

- Very stable
- Shortest time for heat soaking

### Cons
- 5V Power Supply
- 2.5 mm sensing distance
- Difficult to fix and adjust


### Comments

Way to go if you don't bother with the short sensing distance.


## SuperPinda (FYSETC clone)

![](data/probe_accuracy_superpinda_fysetc.jpg)

### Info

- Price: €17,00
- Web: https://de.aliexpress.com/item/1005004421450006.html
- Minimum Heat soaking time: 5 minutes

### Pros

- Best Price/Performance ratio

### Cons

- 5V Power Supply
- 2.5 mm sensing distance
- Deviation can be half of the layer height, without heat soaking.
- Difficult to fix and adjust

### Comments

In many aspects this Z-Probe is a fine replacement for the original parts, specially if considering the price difference.


## OMRON TL-Q5MC2-Z

![](data/probe_accuracy_TL-Q5MC2-Z.jpg)

### Info

- Price: €67,00
- Web: https://www.mouser.at/ProductDetail/Omron-Automation-and-Safety/TL-Q5MC2?qs=SZDmkwkWGmleKATVw1kKHA%3D%3D
- Minimum Heat soaking time: 10 minutes

### Pros

- 5mm sensing distance
- Voron standard

### Cons

- Deviation can be more than the layer height, without heat soaking.
- Price on official reseller are very high


### Comments

This is the official Z-probe used on Voron printer. I cannot recommend this part, since Z changes are as big as one layer. Heat soaking is the only feasible way to use this component. Voron Team should not use this component in any configuration.


## OMRON TL-Q5MC1-Z

![](data/probe_accuracy_TL-Q5MC1-Z.jpg)

### Info

- Price: €67,00
- Web: https://www.mouser.at/ProductDetail/Omron-Automation-and-Safety/TL-Q5MC1?qs=NA0XKeglvRXL5g2iJn2Z1g%3D%3D
- Minimum Heat soaking time: 7 minutes

### Pros

- 5mm sensing distance

### Cons

- Deviation can be more than the layer height, without heat soaking.
- Print head crash on defective installation
- Price on official reseller are very high

### Comments

This is the complementary part offered by OMRON. Similarly it shows abysmal offsets on the Z value. Note that using the "push" feature of the NPN transistor produces more stable readings, but still does not improve for practical application.

Note that although stability of the reading NPN probes has the disadvantage that a nozzle crash happens if some electric connection of the Z-probe fails.


## Panasonic GX-H15A

![](data/probe_accuracy_GX-H15A.jpg)

### Info

- Price: €39,00
- Web: https://www.mouser.at/ProductDetail/Panasonic-Industrial-Automation/GX-H15A?qs=3Rah4i%252BhyCFexaV08Yu2hw%3D%3D
- Minimum Heat soaking time: 5 minutes

### Pros

- 5mm sensing distance
- Best product on this distance sensing
- Very flexible cable

### Cons

- Deviation can be half of the layer height, without heat soaking.
- Print head crash on defective installation

### Comments

I bought this model, since it is from the same family of **Panasonic GX-H12A** and has the advantage of working with more distance.


## Panasonic GX-H12A

![](data/probe_accuracy_GX-H12A.jpg)

### Info

- Price: €27,00
- Web: https://www.mouser.at/ProductDetail/Panasonic-Industrial-Automation/GX-H12A?qs=3Rah4i%252BhyCGaWL%2F65F7Z2A%3D%3D
- Minimum Heat soaking time: 5 minutes

### Pros

- 4mm sensing distance
- Best product on this distance sensing
- Very flexible cable

### Cons

- Deviation can be more than a quarter layer height, without heat soaking.
- Print head crash on defective installation

### Comments

This is the way to go if you want more than 2.5mm sensing distance.


## BAOLSEN N3F-H4NB

![](data/probe_accuracy_N3F-H4NB.jpg)

### Info

- Price: €14,00
- Web: https://de.aliexpress.com/item/1005009091791915.html
- Minimum Heat soaking time: 5 minutes

### Pros

- 4mm sensing distance
- Cheap option for umbilical setup

### Cons

- Deviation can be more than a quarter layer height, without heat soaking.
- Bad experience with long cable harness

### Comments

This is a clone from **Panasonic GX-H12B** commonly found on some chinese 3D printers, like Artillery, Elegoo, SoVol and many other.

My old printer used it with a long cable and noise levels were too high in this situation.


# General Performance Tables

These tables views result in a more general form, not focusing a specific time spot. Each phase of the test was evaluated:
- Overall: Statistics for the entire process
- Phase 1: Statistics for the cold printer (5 minutes)
- Phase 2: Statistics for the warm up phase (until heat-bed reaches target temperature)
- Phase 3: Statistics while hot end and heat bed are stable and sensor is heat soaking (30 minutes)
- Phase 4: Statistics when hot-end and heat bed are turned off and printer cools down (5 minutes)

## Unfiltered Sample Results

This table takes all samples and evaluate statistics. It represents the error associated to use the probe at any random time, without a following a specific procedure.

### Sample Difference (µm)

| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|
| Prusa Super Pinda  |   76.25 |    7.50 |   66.25 |   31.25 |   37.50 |
| FYSETC Super Pinda |  141.25 |   11.25 |  107.50 |   56.25 |   55.00 |
| OMRON TL-Q5MC2-Z   |  230.00 |   15.00 |   67.50 |  156.25 |   95.00 |
| OMRON TL-Q5MC1-Z   |  302.50 |    6.25 |  172.50 |  123.75 |   81.25 |
| Panasonic GX-H15A  |  135.00 |    6.25 |   53.75 |   77.50 |   55.00 |
| Panasonic GX-H12A  |   92.50 |    6.25 |   36.25 |   53.75 |   32.50 |
| BAOLSEN N3F-H4NB   |  101.25 |    6.25 |   57.50 |   50.00 |   38.75 |

### Standard Deviation (µm)

| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|
| Prusa Super Pinda  |   21.73 |    1.82 |   23.15 |    8.93 |    8.45 |
| FYSETC Super Pinda |   39.48 |    2.26 |   37.85 |   17.60 |   19.50 |
| OMRON TL-Q5MC2-Z   |   72.15 |    2.56 |   22.67 |   34.65 |   30.11 |
| OMRON TL-Q5MC1-Z   |   91.69 |    2.05 |   57.87 |   21.68 |   25.25 |
| Panasonic GX-H15A  |   41.91 |    1.76 |   18.60 |   14.25 |   16.03 |
| Panasonic GX-H12A  |   26.98 |    1.26 |   11.67 |   10.78 |    9.05 |
| BAOLSEN N3F-H4NB   |   29.60 |    1.23 |   20.35 |   10.62 |   11.34 |


## Local Sampling Results

This data represents a local data sampling. This considers that Klipper takes a set of samples to compute a single Z value, which reduces noise, in comparison with the general tables.

### Sample Difference (µm)

| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|
| Prusa Super Pinda  |    2.67 |    2.04 |   17.78 |    2.02 |    3.19 |
| FYSETC Super Pinda |    3.21 |    1.09 |   22.44 |    2.86 |    2.67 |
| OMRON TL-Q5MC2-Z   |    7.02 |    5.63 |   18.67 |    6.96 |    6.67 |
| OMRON TL-Q5MC1-Z   |    2.94 |    0.74 |   34.91 |    1.86 |    2.41 |
| Panasonic GX-H15A  |    2.61 |    1.01 |   14.19 |    2.61 |    2.06 |
| Panasonic GX-H12A  |    1.24 |    0.58 |    7.41 |    1.03 |    1.22 |
| BAOLSEN N3F-H4NB   |    3.34 |    2.80 |   15.65 |    2.88 |    3.63 |


### Standard Deviation (µm)

| Z-Probe            | Overall | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|
| Prusa Super Pinda  |    0.89 |    0.71 |    5.80 |    0.68 |    1.06 |
| FYSETC Super Pinda |    1.06 |    0.45 |    7.29 |    0.92 |    0.91 |
| OMRON TL-Q5MC2-Z   |    2.14 |    1.70 |    5.99 |    2.10 |    2.06 |
| OMRON TL-Q5MC1-Z   |    1.01 |    0.29 |   11.23 |    0.66 |    0.85 |
| Panasonic GX-H15A  |    0.86 |    0.40 |    4.59 |    0.84 |    0.71 |
| Panasonic GX-H12A  |    0.46 |    0.22 |    2.43 |    0.39 |    0.47 |
| BAOLSEN N3F-H4NB   |    1.06 |    0.88 |    5.10 |    0.93 |    1.11 |

This tables proves that sampling multiple times makes even the worst probe work within good deviation, when applied to a *local* time spot.


# Heat Soaking Tables

The next set of tables will show how important heat soaking is.  
It focus on **Phase 3** of the previous tables: Instead sampling a random spot, if we apply a reasonable heat soaking time, the first layer results are more deterministic.

## Average Z Value (in mm)

> Take care when interpreting this table. Comparison makes sense only on values of the same row.  
The next table will handle the evolution of these values.

The mean value of the absolute Z reading. 

| Z-Probe            | No Soak | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |
|--------------------|:-------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| Prusa Super Pinda  |  0.0301 | 0.0472 | 0.0463 | 0.0449 | 0.0410 | 0.0384 | 0.0354 | 0.0285 | 0.0240 | 0.0210 |
| FYSETC Super Pinda |  0.1020 | 0.1020 | 0.1070 | 0.1109 | 0.1198 | 0.1261 | 0.1278 | 0.1059 | 0.0907 | 0.0827 |
| OMRON TL-Q5MC2-Z   |  0.1889 | 0.0856 | 0.1133 | 0.1350 | 0.1669 | 0.1798 | 0.2005 | 0.2119 | 0.2107 | 0.2117 |
| OMRON TL-Q5MC1-Z   |  0.2365 | 0.1705 | 0.1997 | 0.2172 | 0.2477 | 0.2641 | 0.2672 | 0.2554 | 0.2412 | 0.2310 |
| Panasonic GX-H15A  |  0.0946 | 0.0580 | 0.0713 | 0.0809 | 0.0950 | 0.1017 | 0.1049 | 0.1025 | 0.0993 | 0.0960 |
| Panasonic GX-H12A  |  0.0330 | 0.0041 | 0.0142 | 0.0226 | 0.0365 | 0.0444 | 0.0486 | 0.0400 | 0.0340 | 0.0294 |
| BAOLSEN N3F-H4NB   |  0.0633 | 0.0308 | 0.0387 | 0.0473 | 0.0637 | 0.0717 | 0.0745 | 0.0706 | 0.0660 | 0.0625 |


## Z Value Evolution (in µm/min)

This is an interesting table, which shows you the evolution of the drift caused by temperature exposure. Practical recommendation is to have offset variation below 1/4 of layer height.  
In general after 10 minutes the drift tends to stabilize and variations are subtle.

| Z-Probe            |  1-2 Min  |  2-3 Min  |  3-5 Min  |  5-7 Min  | 7-10 Min  | 10-15 Min | 15-20 Min | 20-25 Min |
|--------------------|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| Prusa Super Pinda  |    -0.833 |    -1.458 |    -1.954 |    -1.276 |    -1.004 |    -1.372 |    -0.917 |    -0.592 |
| FYSETC Super Pinda |     5.000 |     3.875 |     4.437 |     3.146 |     0.583 |    -4.392 |    -3.033 |    -1.608 |
| OMRON TL-Q5MC2-Z   |    27.667 |    21.750 |    15.938 |     6.437 |     6.903 |     2.275 |    -0.233 |     0.208 |
| OMRON TL-Q5MC1-Z   |    29.208 |    17.583 |    15.208 |     8.208 |     1.056 |    -2.375 |    -2.825 |    -2.058 |
| Panasonic GX-H15A  |    13.375 |     9.583 |     7.042 |     3.333 |     1.069 |    -0.475 |    -0.650 |    -0.642 |
| Panasonic GX-H12A  |    10.042 |     8.417 |     6.979 |     3.938 |     1.389 |    -1.717 |    -1.192 |    -0.925 |
| BAOLSEN N3F-H4NB   |     7.875 |     8.625 |     8.208 |     4.021 |     0.917 |    -0.783 |    -0.908 |    -0.708 |


## Z Value Displacement (Cold to Hot Values in mm)

This table proves that calibrating a printer at cold state is just a waste of time. It shown how much the Z value shifts between a cold system and a soaked probe. Consider that a default layer height is 0.2mm. You can easily tell that Z-offset should never be calibrated in a cold system, regardless of the probe you use. 

Official Voron probe can deviate more than a layer size and I am astonished, why this is the recommended part. 

| Z-Probe            | No Soak | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |
|--------------------|:-------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| Prusa Super Pinda  |  0.0537 | 0.0707 | 0.0699 | 0.0684 | 0.0645 | 0.0620 | 0.0589 | 0.0521 | 0.0475 | 0.0445 |
| FYSETC Super Pinda |  0.1059 | 0.1060 | 0.1110 | 0.1148 | 0.1237 | 0.1300 | 0.1318 | 0.1098 | 0.0946 | 0.0866 |
| OMRON TL-Q5MC2-Z   |  0.1944 | 0.0910 | 0.1187 | 0.1405 | 0.1723 | 0.1852 | 0.2059 | 0.2173 | 0.2161 | 0.2172 |
| OMRON TL-Q5MC1-Z   |  0.2685 | 0.2025 | 0.2317 | 0.2492 | 0.2797 | 0.2961 | 0.2992 | 0.2874 | 0.2732 | 0.2630 |
| Panasonic GX-H15A  |  0.1186 | 0.0820 | 0.0954 | 0.1050 | 0.1191 | 0.1257 | 0.1289 | 0.1266 | 0.1233 | 0.1201 |
| Panasonic GX-H12A  |  0.0733 | 0.0444 | 0.0545 | 0.0629 | 0.0768 | 0.0847 | 0.0889 | 0.0803 | 0.0743 | 0.0697 |
| BAOLSEN N3F-H4NB   |  0.0843 | 0.0518 | 0.0597 | 0.0683 | 0.0848 | 0.0928 | 0.0956 | 0.0916 | 0.0871 | 0.0836 |

> Even the best probe produces a significant layer shift.


## Standard Deviation (µm)

The classic standard deviation gives a picture of the noise average that is expected.

| Z-Probe            | No Soak | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |
|--------------------|:-------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| Prusa Super Pinda  |   8.909 |  0.909 |  0.786 |  0.875 |  0.882 |  0.850 |  0.737 |  0.728 |  0.652 |  0.595 |
| FYSETC Super Pinda |  17.628 |  2.360 |  2.177 |  1.852 |  2.143 |  1.007 |  0.786 |  1.375 |  1.194 |  0.954 |
| OMRON TL-Q5MC2-Z   |  40.133 |  7.561 |  7.572 |  7.688 |  3.829 |  3.012 |  2.250 |  1.638 |  2.229 |  1.953 |
| OMRON TL-Q5MC1-Z   |  33.999 | 12.676 |  5.636 |  4.737 |  3.732 |  1.161 |  0.500 |  1.028 |  1.021 |  0.529 |
| Panasonic GX-H15A  |  14.249 |  4.114 |  3.369 |  2.886 |  1.677 |  0.812 |  0.747 |  0.913 |  0.692 |  0.567 |
| Panasonic GX-H12A  |  12.436 |  2.996 |  2.820 |  2.370 |  1.603 |  1.057 |  0.425 |  0.456 |  0.529 |  0.624 |
| BAOLSEN N3F-H4NB   |  11.547 |  1.564 |  2.904 |  3.046 |  0.994 |  1.392 |  0.829 |  0.898 |  0.973 |  0.791 |

*In general if a system is calibrated on a very specific time spot, from a common starting temperature, every Z-probe is able to produce a decent first layer. Prusa and Panasonic are really more stable than other models and Panasonic tends to be better after enough soaking, since its sensing distance is bigger, requiring less mechanical trimming to apply it.*


## Amplitude Difference (µm)

The min an max Z values, may contaminate single samples, causing spurious hill or valleys.

| Z-Probe            | No Soak | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 7 Min  | 10 Min | 15 Min | 20 Min | 25 Min |
|--------------------|:-------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| Prusa Super Pinda  |   33.75 |   2.50 |   3.75 |   2.50 |   3.75 |   3.75 |   2.50 |   2.50 |   2.50 |   2.50 |
| FYSETC Super Pinda |   66.25 |   8.75 |  10.00 |   6.25 |   7.50 |   3.75 |   2.50 |   5.00 |   5.00 |   3.75 |
| OMRON TL-Q5MC2-Z   |  183.75 |  26.25 |  31.25 |  31.25 |  15.00 |  13.75 |  10.00 |   8.75 |   8.75 |   7.50 |
| OMRON TL-Q5MC1-Z   |  231.25 |  43.75 |  18.75 |  16.25 |  12.50 |   3.75 |   1.25 |   3.75 |   2.50 |   1.25 |
| Panasonic GX-H15A  |   77.50 |  15.00 |  11.25 |  11.25 |   7.50 |   2.50 |   3.75 |   5.00 |   2.50 |   2.50 |
| Panasonic GX-H12A  |   65.00 |  10.00 |  10.00 |   7.50 |   5.00 |   3.75 |   1.25 |   2.50 |   1.25 |   1.25 |
| BAOLSEN N3F-H4NB   |   51.25 |   6.25 |  11.25 |  11.25 |   3.75 |   5.00 |   3.75 |   3.75 |   3.75 |   2.50 |

*Some probes are useless without a considerable heat soaking. It is impressive how physical size of the sensor affects directly these values.*


# Conclusions

In general mechanical resolution of the Z axis, which is 1.25 µm, rules the standard deviation measured *locally* and a maximum drift of 1/4 of the layer height is a common sense on forums.

Some points can be listed:
- Not a single Probe should be used without heat soaking
- Prusa SuperPinda (**Warning:** 5V power supply!!) is the only exception that will produce decent results already with 3 minutes soaking.
- For OMRON probes, and if you still don't want to replace it, consider heat soaking for at least 7 minutes.
- For all other probes:
  - A coarse heat soaking routine should start sample at 3 minutes.
  - A acceptable heat soaking routine should sample at 5 minutes.
  - If you want a cheap option:
    - Go with SuperPinda FYSETC (**Warning:** 5V power supply!!)
	- Baolsen N3F-H4NB (easier to find) for umbilical setup only
	- Baolsen N3F-H4NA for long cable harness (untested, but should behave similar to complementary part)
- Switch distance of the sensor affects it's stability. SuperPinda is a 2.5mm sensor and shines on every test. 
- Panasonic is the way to go for 4mm or 5.5 mm sensors, which is also easier to adjust.
- Printers with umbilical setup can use complementary parts (*normally closed*) of the parts tested here. Shorter cables will keep noise levels in acceptable range. The advantage is that a defect on the sensor connection will not cause a head crash.  
In *normally open* sensors switching signal is very precise, but defective wiring will cause a head crash.
- The Baolsen Sensor is used on some printers from Artillery, Elegoo and Sovol, works quite good on an umbilical setup. But, my experience with them on longer cables was a deception.
- Voron Team should remove **TL-Q5MC2-Z** probe from their listing. For example, Panasonic **GX-H15A** has the same sensing distance as **TL-Q5MC2-Z** and is outstanding, with lower price.

