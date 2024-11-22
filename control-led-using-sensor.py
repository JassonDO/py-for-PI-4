import paho.mqtt.client as mqtt
from gpiozero import LED
from grove.display.jhd1802 import JHD1802

lcd = JHD1802()

# Cấu hình ThingSpeak MQTT
channel_id = "2665872"  # Thay bằng ID của bạn
mqtt_host = "mqtt3.thingspeak.com"
mqtt_port = 1883
mqtt_username = "KzMSOjsQARoEBjwwDxkqIiI"  # Thay bằng API Key MQTT của bạn
mqtt_password = "FO7WCP86JLY7YPeBaL9MlF+g"  # Thay bằng mật khẩu MQTT
client_id = "KzMSOjsQARoEBjwwDxkqIiI"  # Thay bằng Client ID của bạn

# Các trường dữ liệu mà bạn muốn đăng ký
field1 = "field1"
field2 = "field2"

# Thiết lập LED ở chân GPIO D22
led = LED(22)

# Hàm này sẽ được gọi khi client kết nối với broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully with result code {rc}")
        # Đăng ký chủ đề cho các trường dữ liệu
        topic1 = f"channels/{channel_id}/subscribe/fields/{field1}"
        client.subscribe(topic1)
        topic2 = f"channels/{channel_id}/subscribe/fields/{field2}"
        client.subscribe(topic2)
        print(f"temp avg: {topic1} | hum avg: {topic2}")
    else:
        print(f"Connection failed with result code {rc}")

# Hàm này sẽ được gọi khi nhận được tin nhắn
def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")
    # Kiểm tra nếu tin nhắn đến từ trường nhiệt độ
    if field1 in msg.topic:
        try:
            temp = float(msg.payload.decode())
            lcd.setCursor(0,0)
            lcd.write(f'Nhiet do {temp}')
            print(f"Nhiet do: {temp}°C")
            # Nếu nhiệt độ > 25, tắt LED; ngược lại bật LED
            if temp > 25:
                led.on()
                print('Led on')
            elif temp < 24:
                led.off()
                print('Led off')
        except ValueError:
            print("Invalid temperature data")
    if field2 in msg.topic:
        hum=float(msg.payload.decode())
        lcd.setCursor(1,0)
        lcd.write(f'Do am {hum}%')
        print(f"Do am: {hum}%")
# Tạo một đối tượng MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
# Thiết lập username và password cho kết nối MQTT
client.username_pw_set(username=mqtt_username, password=mqtt_password)
# Gán các hàm callback on_connect và on_message
client.on_connect = on_connect
client.on_message = on_message
# Kết nối với broker ThingSpeak MQTT
client.connect(mqtt_host, mqtt_port, 60)
# Khởi động vòng lặp MQTT để liên tục theo dõi tin nhắn
client.loop_forever()