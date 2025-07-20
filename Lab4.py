from seeed_dht import DHT
import time

import paho.mqtt.client as mqtt

sensor = DHT('11', 5)


# Thông tin tài khoản MQTT và client ID
username = "MSYAByc0MTsqLhICEjgmNB0"
clientId = "MSYAByc0MTsqLhICEjgmNB0"
password = "WDC0w9yDy3G3UbMGLMhiMja+"

# Khởi tạo client MQTT với MQTTv5
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, clientId)

# Cấu hình username và password
client.username_pw_set(username=username, password=password)

# Đăng ký callback để xem kết nối có thành công không
def on_connect(client, userdata, flags, reasonCode, properties=None):
    print(f"Connected with result code {reasonCode}")

client.on_connect = on_connect

# Kết nối tới MQTT broker
client.connect("mqtt3.thingspeak.com", 1883, 60)

# Hàm gửi dữ liệu lên ThinkSpeak qua MQTT
def thinkspeak_mqtt(data1,data2):
    channel_ID = "2665872"
    topic = f"channels/{channel_ID}/publish"
    payload = f"field1={data1}&field2={data2}&status=MQTTPUBLISH"
    

    # Gửi dữ liệu với topic và payload chính xác
    client.publish(topic, payload)

# Khởi tạo danh sách để lưu trữ các giá trị nhiệt độ và độ ẩm
temperature_readings = []
humidity_readings = []

# Hàm giả lập đọc dữ liệu từ cảm biến
def read_sensor_data():
    # Thay thế đoạn code này bằng việc đọc dữ liệu thực từ mô-đun Grove
    humidity,temperature = sensor.read()

    return temperature, humidity

# Hàm tính giá trị trung bình của danh sách
def calculate_average(readings):
    if readings:
        return sum(readings) / len(readings)
    else:
        return 0

# Vòng lặp chính
#start_time = time.time()
#while time.time() - start_time < 30 * 60:  # Chạy liên tục trong 30 phút
while True:
    # Đọc giá trị nhiệt độ và độ ẩm từ cảm biến
    temp, hum = read_sensor_data()
    
    # Thêm giá trị vào danh sách
    temperature_readings.append(temp)
    humidity_readings.append(hum)

    # Hiển thị giá trị nhiệt độ và độ ẩm lên dòng đầu của LCD
    print(f"Temperature: {temp}C, Humidity: {hum}%")
    # Đợi 2 giây trước khi đọc lần tiếp theo
    time.sleep(1)

    # Tính toán trung bình mỗi 20 giây
    if len(temperature_readings) >= 20:  # Vì mỗi 20 giây có 10 lần đo (2 giây một lần)
        avg_temp = calculate_average(temperature_readings)
        avg_hum = calculate_average(humidity_readings)
        
        # Hiển thị giá trị trung bình lên dòng thứ hai của LCD
        print(f"Avg Temp: {avg_temp}C, Avg Hum: {avg_hum}%")
        time.sleep(2)
        # Gửi dữ liệu lên ThingSpeak ()
        thinkspeak_mqtt(avg_temp,avg_hum)


        # Xóa dữ liệu trong danh sách để chuẩn bị cho chu kỳ tiếp theo
        temperature_readings.clear()
        humidity_readings.clear()
    
