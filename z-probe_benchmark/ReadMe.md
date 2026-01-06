# Charts

These charts shows a stress test for different Z-Probe values.

The black line is the Z value, which the absolute value is meaningless, since this is the difference of the Z-endstop switch and the Z-probe. This is calibrated using screws and no different mount is repeatable. But difference is important.

The blue line shows the temperature of the head bed, which tends to shift the Z-Probe readings because of thermal expansion. The behavior of the Z curve shows how fine a temperature compensation compensation circuit is.

The red line shows temperature for the hot end, which is usually very near to the Z-probe and also influences Z readings, similar to the heat bed.

The graph shows `Z10+ diff` and `Z10+ stddev` values, simulating a heat soak of 10 minutes on the red area.


## SuperPinda (Prusa / Pepperl&Fuchs)

![](data/probe_accuracy_superpinda.jpg)

Although SuperPinda is very famous, temperature changes may have sufficient influence to cause issues on the first layer.


## SuperPinda (FYSETC clone)

![](data/probe_accuracy_superpinda_fysetc.jpg)

In many aspects this Z-Probe is a fine replacement, specially if considering the price difference.


## OMRON TL-Q5MC2-Z

![](data/probe_accuracy_TL-Q5MC2-Z.jpg)

This is th official Z-probe used on Voron printer. I cannot recommend this part, since Z changes are as big as one layer. Heat soaking is the only feasible way to use this component.


## OMRON TL-Q5MC1-Z

![](data/probe_accuracy_TL-Q5MC1-Z.jpg)

This is the complementary part offered by OMRON. Similarly it shows abismal offsets on the Z value. Note that using the "push" feature of the NPN transistor produces more stable readings, but still does not improve for practical application.

Note that although stability of the reading NPN probes has the disadvantage that a nozzle crash happens if some electric connection of the Z-probe fails.

Heat soaking is mandatory.


# Heat Soaking Tables

## Average Z Value (in mm)

The mean value of the absolute Z reading. 

| Z-Probe            | No Soak | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 10 Min |
|--------------------|:-------:|:------:|:------:|:------:|:------:|:------:|
| Prusa Super Pinda  | 1.5381  | 1.5375 | 1.5371 | 1.5369 | 1.5366 | 1.5358 |
| FYSETC Super Pinda | 0.8885  | 0.8876 | 0.8862 | 0.8848 | 0.8825 | 0.8788 |
| OMRON TL-Q5MC2-Z   | 2.8547  | 2.8572 | 2.8590 | 2.8604 | 2.8621 | 2.8635 |
| OMRON TL-Q5MC1-Z   | 2.1258  | 2.1273 | 2.1274 | 2.1270 | 2.1252 | 2.1197 |

*It is meaningless to compare different rows. Use it to compare the evolution according to heat soak time.*


## Z Value Displacement (Cold to Hot Values in mm)

This table is more important than the previous. It shown how much the Z value shifts between a cold system and a soaked probe. Consider that a default layer height is 0.2 mm and you can easily tell when a probe is poor, if not soaked.

| Z-Probe            | No Soak | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 10 Min |
|--------------------|:-------:|:------:|:------:|:------:|:------:|:------:|
| Prusa Super Pinda  |  0.0366 | 0.0360 | 0.0356 | 0.0354 | 0.0351 | 0.0344 |
| FYSETC Super Pinda |  0.0702 | 0.0693 | 0.0679 | 0.0665 | 0.0642 | 0.0605 |
| OMRON TL-Q5MC2-Z   |  0.2140 | 0.2165 | 0.2183 | 0.2197 | 0.2214 | 0.2228 |
| OMRON TL-Q5MC1-Z   |  0.1947 | 0.1963 | 0.1964 | 0.1960 | 0.1942 | 0.1886 |

*Prusa Super Pinda is a leap forward.*


## Standard Deviation (µm)

The classic standard deviation gives a picture of the noise average that is expected.

| Z-Probe            | No Soak | 1 Min  | 2 Min  | 3 Min  | 5 Min  | 10 Min |
|--------------------|:-------:|:------:|:------:|:------:|:------:|:------:|
| Prusa Super Pinda  |  3.0130 | 2.0204 | 1.4497 | 1.3144 | 1.1678 | 0.9506 |
| FYSETC Super Pinda |  9.8947 | 9.4208 | 8.2352 | 6.7604 | 4.6141 | 2.3757 |
| OMRON TL-Q5MC2-Z   | 12.7220 | 9.2573 | 6.6763 | 4.8226 | 2.8565 | 2.0003 |
| OMRON TL-Q5MC1-Z   |  8.9575 | 6.7112 | 6.8881 | 6.9792 | 6.3167 | 2.6888 |

*In general if a system is calibrated on a very specific temperature and enough time is given for stability, on every print or calibrate, every Z-probe is able to produce a decent first layer. Prusa Super Pinda is a leap forward and tolerate not strictly controlled use cases.*


## Amplitude Difference (µm)

The min an max Z values, may contaminate single samples, causing spurious hill or valleys.

| Z-Probe            | No Soak |  1 Min  |  2 Min  |  3 Min  |  5 Min  |  10 Min |
|--------------------|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|
| Prusa Super Pinda  | 14.6870 | 13.1250 |  8.4370 |  7.5000 |  6.5620 |  5.3120 |
| FYSETC Super Pinda | 32.8130 | 32.8130 | 30.3130 | 26.8750 | 18.1250 |  8.1250 |
| OMRON TL-Q5MC2-Z   | 55.6250 | 39.6870 | 32.5000 | 24.3750 | 14.6870 |  9.3750 |
| OMRON TL-Q5MC1-Z   | 48.4370 | 21.5620 | 21.5620 | 21.5620 | 21.2500 | 10.0000 |





