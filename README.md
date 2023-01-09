# NTC_MF52AT_3950k_10kOhm thermistor micropython driver

### requires:
[micropython version: >= v1.19.1](https://micropython.org/download/rp2-pico/)
Assumes use of 10kΩ nominal [NTC_MF52 thermistors](https://www.gotronic.fr/pj2-mf52type-1554.pdf)

### other imports:
``` python
from machine import Pin
import time
from NTC_MF52 import NTC_MF52AT_3950k_10kOhm as thermistor_setup
```

### user configuration:

1. set the pins you intend to use for ADC Pin(27)
2. configure adc depth, default (16 bit == 0-65536 raspberry pico)  
3. measure and enter supply voltage across your voltage divider (default:3.3)
4. enter the max expected amperage (default 2.0)


### code to configure in main.py to run thermistor on 
```python
adc_pin = Pin(27)  # <int> 31 & 32 & 34 (GPs 26,27,28) are the only pins for ADC
adc_depth = 65536   # <int> 2^bit_depth of ADC
supply_voltage = 3.263  # <float> supply voltage measured
known_divider_resistance = 9880  # <int> measured resistance in Ohms
```

### voltage divider circuit to measure

![voltage_divider_circuit](/imgs/NTC_MF52_Thermistor.png "NTC_MF52 Thermistor Voltage Divider Circuit")