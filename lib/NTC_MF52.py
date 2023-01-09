# The MIT License (MIT)
#
# Copyright (c) 2023 Dean Sanders 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from machine import ADC
import math

class NTC_MF52AT_3950k_10kOhm:
    def __init__(self,input_pin,supply_voltage,known_resistor) -> None:
        self.adc = ADC(input_pin)
        self.supply_voltage = supply_voltage
        self.divider_known_resistance = known_resistor
        self.adc_depth = 65535
        self.bias = 0.016

    def map_val(value, istart, istop, ostart, ostop):
        return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

    def get_temp_in_F(self):
        adc_raw_reading = self.adc.read_u16()
        #TODO: measure the voltage across a 10kOhm resistor
        divider_voltage = round(adc_raw_reading,0,self.adc_depth,0.000,self.supply_voltage),6)
        #TODO: determine total current flowing through the voltage divider
        # V=IR
        I = divider_voltage/self.divider_known_resistance
        #TODO: based on I, determine the voltage across the thermistor
        thermistor_voltage = self.supply_voltage - divider_voltage
        #TODO: back calculate the resistance of the thermistor
        thermistor_resistance = thermistor_voltage/I
        thermistor_resistance_kohm = thermistor_resistance/1000
        #TODO: map thermistor resistance to temp
        """
        NTC-MF52AT 3950k 10kOhm
        y is resistance and x is temp in F:
        y = -23.64*ln(x) + 112.7
        therefore to get temp in F:
        x = e^(-(y-112.7)/23.64)
        =EXP(-((y-112.7)/23.64))
        """
        temp_F = math.e**(-(thermistor_resistance_kohm - 112.7)/23.64)
        tuple_output = (temp_F,thermistor_resistance_kohm)
        return tuple_output

