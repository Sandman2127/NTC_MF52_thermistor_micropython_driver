from machine import Pin
import time
from NTC_MF52 import NTC_MF52AT_3950k_10kOhm as thermistor_setup

adc_pin = Pin(27)  # <int> 31 & 32 & 34 (GPs 26,27,28) are the only pins for ADC
adc_depth = 65536   # <int> 2^bit_depth of ADC
supply_voltage = 3.263  # <float> supply voltage measured
known_divider_resistance = 9880  # <int> measured resistance in Ohms

def get_date_time():
    timelist = time.localtime()
    _date = str(timelist[0]) + "-" + str(timelist[1]) + "-" + str(timelist[2])
    _time = str(timelist[3]) + ":" + str(timelist[4]) + ":" + str(timelist[5])
    out = [_date,_time]
    return out

# setup thermistor
thermistor_1 = thermistor_setup(adc_pin,supply_voltage,known_divider_resistance)

if __name__ == '__main__':
    while True:
        #TODO: check_voltage_convert_to_temp
        tuple_out = thermistor_1.get_temp_in_F()
        temperature,thermistor_resistance_kohm = tuple_out[0],tuple_out[1]
        #TODO: get time and date:
        date_time_list = get_date_time()
        _date,_time = date_time_list[0],date_time_list[1]
        #TODO: print out data:
        print("")
        print("Date:",_date)
        print("Time:",_time)
        print("Temperature:",temperature,"F")
        print("Thermistor Resistance:",thermistor_resistance_kohm,"kOhm")
        print("Formula: Temp in Farenheit = e**(-(",str(thermistor_resistance_kohm),"- 112.7 ) / 23.64 )")
        print("")
        time.sleep(120)