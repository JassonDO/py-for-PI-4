from seeed_dht import DHT
import time
from datetime import timedelta
from datetime import datetime
import paho.mqtt.client as mqtt
from gpiozero import LED
from urllib import request, parse

# Khởi tạo cảm biến và LED
sensor = DHT('11', 5)
led = LED(22)

# Cấu hình MQTT cho tài khoản 1 (upload dữ liệu)
channel_id_1 = "2665876"  # Thay bằng ID của bạn cho tài khoản 1
mqtt_host_1 = "mqtt3.thingspeak.com"
mqtt_port_1 = 1883
mqtt_username_1 = "MjUoDwQXEQcBEQQgIysnMRg"  # Thay bằng API Key MQTT của bạn (tài khoản 1)
mqtt_password_1 = "9Ubc5eJNLELGWu36VyaZroDM"  # Thay bằng mật khẩu MQTT (tài khoản 1)
client_id_1 = "MjUoDwQXEQcBEQQgIysnMRg"  # Thay bằng Client ID của bạn (tài khoản 1)

# Cấu hình MQTT cho tài khoản 2 (download dữ liệu)
channel_id_2 = "2707006"  # Thay bằng ID của bạn cho tài khoản 2
mqtt_host_2 = "mqtt3.thingspeak.com"
mqtt_port_2 = 1883
mqtt_username_2 = "CxgcOTY7BA8oCSIwNS4zDBs"  # Thay bằng API Key MQTT của bạn (tài khoản 2)
mqtt_password_2 = "ZnFmMDRWiZIjBsWxJI4tbXr0"  # Thay bằng mật khẩu MQTT (tài khoản 2)
client_id_2 = "CxgcOTY7BA8oCSIwNS4zDBs"  # Thay bằng Client ID của bạn (tài khoản 2)

channel_id_3 = "2715612"  # Thay bằng ID của bạn cho tài khoản 2
mqtt_host_3 = "mqtt3.thingspeak.com"
mqtt_port_3 = 1883
mqtt_username_3 = "MzAJKx82KQw7BAgNFhojIBk"  # Thay bằng API Key MQTT của bạn (tài khoản 2)
mqtt_password_3 = "Eg4d/818dLHtwNzmhSffLOpB"  # Thay bằng mật khẩu MQTT (tài khoản 2)
client_id_3 = "MzAJKx82KQw7BAgNFhojIBk"

channel_id_4 = "2715612"  # Thay bằng ID của bạn cho tài khoản 2
mqtt_host_4 = "mqtt3.thingspeak.com"
mqtt_port_4 = 1883
mqtt_username_4 = "Cg02JQgsATApCxwaDiUiFyA"  # Thay bằng API Key MQTT của bạn (tài khoản 2)
mqtt_password_4 = "hGT7nCL6FXxwee0XMTMW60d5"  # Thay bằng mật khẩu MQTT (tài khoản 2)
client_id_4 = "Cg02JQgsATApCxwaDiUiFyA" 

# MQTT client cho tài khoản 1 (upload)
client_1 = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id_1)
client_1.username_pw_set(username=mqtt_username_1, password=mqtt_password_1)

# MQTT client cho tài khoản 2 (download)
client_2 = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id_2)
client_2.username_pw_set(username=mqtt_username_2, password=mqtt_password_2)

client_3 = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id_3)
client_3.username_pw_set(username=mqtt_username_3, password=mqtt_password_3)

client_4 = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id_4)
client_4.username_pw_set(username=mqtt_username_4, password=mqtt_password_4)
# Tài khoản 1 (Client 1) sẽ upload dữ liệu
def thinkspeak_mqtt_1(data1, data2):
    topic = f"channels/{channel_id_1}/publish"
    payload = f"field1={data1}&field2={data2}&status=MQTTPUBLISH"
    client_1.publish(topic, payload)

def thinkspeak_mqtt_3(data3, data4):
    topic = f"channels/{channel_id_3}/publish"
    payload = f"field1={data3}&field2={data4}&status=MQTTPUBLISH"
    client_3.publish(topic, payload)
    
# Tài khoản 2 (Client 2) sẽ download dữ liệu từ field1 và field2
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully with result code {rc}")
        # Đăng ký nhận dữ liệu từ field1 và field2
        topic = f"channels/{channel_id_2}/subscribe/fields/field1"
        client.subscribe(topic)
    else:
        print(f"Connection failed with result code {rc}")

def on_connect_4(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully with result code {rc}")
        # Đăng ký nhận dữ liệu từ field1 và field2
        topic1 = f"channels/{channel_id_4}/subscribe/fields/field1"
        topic2 = f"channels/{channel_id_4}/subscribe/fields/field2"
        client.subscribe(topic1)
        client.subscribe(topic2)
    else:
        print(f"Connection failed with result code {rc}")

def on_message(client, userdata, msg):
    print(f"Received {msg.payload.decode()}")
    # Xử lý dữ liệu từ field1 (nhiệt độ)
    if "field1" in msg.topic:
        try:
            flag = float(msg.payload.decode())
            if flag==1:
                led.on()
            else:
                led.off()
        
        except ValueError:
            print("Invalid temperature data")

# Gán callback cho client 2 (download)
client_1.on_connect = on_connect
client_2.on_connect = on_connect
client_2.on_message = on_message
client_4.on_connect_4= on_connect_4
# Kết nối tài khoản 1 và tài khoản 2
client_1.connect(mqtt_host_1, mqtt_port_1, 60)
client_2.connect(mqtt_host_2, mqtt_port_2, 60)
client_3.connect(mqtt_host_3, mqtt_port_3, 60)
client_4.connect(mqtt_host_4, mqtt_port_4, 60)
temperature_readings = []
humidity_readings = []

def read_sensor_data():
    humidity, temperature = sensor.read()
    return temperature, humidity

def calculate_average(readings):
    if readings:
        return sum(readings) / len(readings)
    return 0

# Vòng lặp chính
while True:
    # Đọc dữ liệu từ cảm biến
    temp, hum = read_sensor_data()
    temperature_readings.append(temp)
    humidity_readings.append(hum)

    print(f"Temperature: {temp}C, Humidity: {hum}%")
    thinkspeak_mqtt_3(temp, hum)
    time.sleep(1)
    # Sau khi có 20 lần đọc, tính giá trị trung bình và upload
    if len(temperature_readings) >= 20:
        avg_temp = calculate_average(temperature_readings)
        avg_hum = calculate_average(humidity_readings)

        print(f"Avg Temp: {avg_temp}C, Avg Hum: {avg_hum}%")
        thinkspeak_mqtt_1(avg_temp, avg_hum)  # Tài khoản 1 upload dữ liệu

        temperature_readings.clear()
        humidity_readings.clear()
    
    # Tài khoản 2 download dữ liệu
    client_2.loop_start()
    client_4.loop_start()