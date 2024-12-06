# control led using DHT11, Light sensor, GroveUltrasonicRanger, RotaryAngel sensor,
# and then show information on LCD 16x2

from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
from time import sleep
from grove.grove_relay import GroveRelay
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from gpiozero import  LED
from grove.adc import ADC
import sys
import math

led3=LED(22)
led2= LED(18)
led1 = LED(16)
state1=False
state2=False
state3=False
led_state1=False
led_state2=False
led_state3=False
lcd = JHD1802()
sensor1 = DHT('11', 24)
sensor2 = ADC()
ur = GroveUltrasonicRanger(5)
rl = GroveRelay(12)

sensor_pin = 0
class GroveLightSensor:
    def __init__(self, chanel):
        self.chanel = chanel
        self.adc = ADC()
        
    @property
        
    def light(self):
        value = self.adc.read(self.chanel)
        return value

sensor = GroveLightSensor(sensor_pin)    
    

def hienthi():
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.write(f't:{nhiet_do},h:{do_am},as:{sensor.light}')
    lcd.setCursor(1,0)
    lcd.write(f'ur:{fkc},v:{value}')
    print("{} cm".format(fkc))
    print("Nhiet do: {} do C, Do am: {} %".format(nhiet_do, do_am))
    print("gia tri anh sang: {0}".format(sensor.light))
    print("gia tri bien tro : {0}".format(value))
def sosanh_t():
    global led_state1
    if nhiet_do > 29:
        led1.on()
        led_state1=True
            
    if nhiet_do < 27:
        led_state1=False
        led1.off()
def sosanh_h():
    global led_state2
    if do_am > 90:
        led2.on()
        led_state2=True
            
    if do_am < 80:
        led_state2=False
        led2.off()
def sosanh_bt   ():
    global led_state3
    if value > 2:
        led3.on()
        led_state3=True
            
    if value < 1.5:
        led_state3=False
        led3.off()
while True:
    
    value=sensor2.read_voltage(4)/1000
    do_am, nhiet_do = sensor1.read()
    kc = ur.get_distance()
    fkc=round(kc,1)
    hienthi()
    sosanh_t()
    if state1 != led_state1:
        if led_state1==True:
            print(f"led1:on, nhiet do: {nhiet_do}")
            lcd.clear()
            lcd.write(f'led1:on t:{nhiet_do}')
            state1=led_state1
            sleep(3)
        else:
            print(f"led1:off, nhiet do: {nhiet_do}")
            lcd.clear()
		  lcd.setCursor(0, 0)
            lcd.write(f'led1:off t:{nhiet_do}')
            state1=led_state1
            sleep(3)
    sosanh_h()
    if state2 != led_state2:
        if led_state2==True:
            print(f"led2:on, do am: {do_am}")
            lcd.clear()
            lcd.setCursor(0,0)
            lcd.write(f' led2:on')
            lcd.setCursor(1,0)
            lcd.write(f'do am: {do_am}')
            state2=led_state2
            sleep(3)
        else:
            print(f"led2:off, do am: {do_am}")
            lcd.clear()
            lcd.setCursor(0,0)
            lcd.write(f' led2:off')
            lcd.setCursor(1,0)
            lcd.write(f'do am: {do_am}')
            state2=led_state2
            sleep(3)
    sosanh_bt() 
    if state3 != led_state3:
        if led_state3==True:
            print(f"led3:on, bien tro : {value}")
            lcd.clear()
            lcd.setCursor(0,0)
            lcd.write(f' led3:on')
            lcd.setCursor(1,0)
            lcd.write(f'bien tro {value}')
            state3=led_state3
            sleep(3)
        else:
            print(f"led3:off, bien tro : {value}")
            lcd.clear()
            lcd.setCursor(0,0)
            lcd.write(f' led3:off')
            lcd.setCursor(1,0)
            lcd.write(f'bien tro {value}')
            state3=led_state3
            sleep(3)
