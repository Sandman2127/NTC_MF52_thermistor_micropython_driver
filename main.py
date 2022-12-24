from machine import Pin
import time,math


adc_pin = machine.Pin(27)  #31 & 32 & 34 (GPs 26,27,28) are the only pins for ADC ones
adc = machine.ADC(adc_pin)
adcDepth = 65536
inputVoltage = 3.263

def map_val(value, istart, istop, ostart, ostop):
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def get_adc_reading():
    #TODO: take ADC reading int 0 - 4096
    adcRawReading = adc.read_u16()
    #TODO: map and remove 16 mV bias, comes out as 0.0010257...
    _10k_Voltage = round(map_val(adcRawReading,0,adcDepth,0.000,inputVoltage),6)
    #TODO: total current
    # V=IR
    I = _10k_Voltage/9880
    # convert to thermistor resistance
    thermistor_voltage = inputVoltage - _10k_Voltage
    thermistor_resistance = thermistor_voltage/I
    thermistor_resistance_kohm = thermistor_resistance/1000
    """
    NTC-MF52AT 3950k 
    y is resistance and x is temp in F:
    y = -23.64*ln(x) + 112.7
    therefore to get temp in F:
    x = e^(-(y-112.7)/23.64)
    =EXP(-((y-112.7)/23.64))
    """
    # calculate based on logarithmic curve the temp in farenheit
    #print(thermistor_resistance_kohm)
    temp_F = math.e**(-(thermistor_resistance_kohm - 112.7)/23.64)
    listout = [temp_F,thermistor_resistance_kohm]
    return listout


if __name__ == '__main__':
    while True:
        #TODO: check_voltage_convert_to_temp
        listout = get_adc_reading()
        temperature,thermistor_resistance_kohm = listout[0],listout[1]
        print("")
        print("Temperature:",temperature,"F")
        print("Thermistor Kohm:",thermistor_resistance_kohm,"Ohm")
        print("Formula: x = e^(-(therm_kOhm - 112.7)/23.64)")
        print("")
        time.sleep(120)