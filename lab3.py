# Write code for control Raspberry Pi 4
# connect to Grove Base Hat module to read
# temperature, humidity after 2 second.
# Then show that to LCD 16x2,
# calculate the average value of 
# temperature and humidity every 20 second. 
# Send data to thingspeak. using MQTT

# channel_ID = "2665872"
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
import time
from grove.grove_relay import GroveRelay

import paho.mqtt.client as mqtt
from random import randint

lcd = JHD1802()
sensor = DHT('11', 5)

username = "MSYAByc0MTsqLhICEjgmNB0"
clientId = "MSYAByc0MTsqLhICEjgmNB0"
password = "WDC0w9yDy3G3UbMGLMhiMja+"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, clientId)

client.username_pw_set(username=username, password=password)

def on_connect(client, userdata, flags, reasonCode, properties=None):
    print(f"Connected with result code {reasonCode}")

client.on_connect = on_connect

client.connect("mqtt3.thingspeak.com", 1883, 60)

def thinkspeak_mqtt(data1,data2):
    channel_ID = "2665872"
    topic = f"channels/{channel_ID}/publish"
    payload = f"field1={data1}&field2={data2}&status=MQTTPUBLISH"
    

    client.publish(topic, payload)

temperature_readings = []
humidity_readings = []

def read_sensor_data():
   
    humidity,temperature = sensor.read()
    return temperature, humidity

def calculate_average(readings):
    if readings:
        return sum(readings) / len(readings)
    else:
        return 0

 
# Vòng lặp chính
#start_time = time.time()
#while time.time() - start_time < 30 * 60:  # Chạy liên tục trong 30 phút
while True:
    lcd.clear()
    temp, hum = read_sensor_data()
    
    temperature_readings.append(temp)
    humidity_readings.append(hum)

    lcd.setCursor(0,0)
    lcd.write(f" t:{temp}C, h:{hum}%")
    print(f"Temperature: {temp}C, Humidity: {hum}%")
    time.sleep(2)

   
    if len(temperature_readings) >= 10:  # Vì mỗi 20 giây có 10 lần đo (2 giây một lần)
        avg_temp = calculate_average(temperature_readings)
        avg_hum = calculate_average(humidity_readings)
        
        lcd.setCursor(1,0)
        lcd.write(f"at{avg_temp}C,ah{avg_hum}%")
        print(f"Avg Temp: {avg_temp}C, Avg Hum: {avg_hum}%")
        time.sleep(2)
        thinkspeak_mqtt(avg_temp,avg_hum)

        temperature_readings.clear()
        humidity_readings.clear()
