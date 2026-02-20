# ========================
# IMPORT REQUIRED LIBRARIES
# ========================
import network
import urequests
import utime
import ujson
from machine import Pin, I2C
from lcd import Lcd_i2c


# ========================
# CONFIGURATION
# ========================
CONFIG_FILE = "config.json"
I2C_SDA = 0
I2C_SCL = 1
I2C_ADDR = 0x27
WEATHER_UPDATE_INTERVAL = 600  # 10 minutes


# ========================
# LOAD CONFIG
# ========================
def load_config():
    with open(CONFIG_FILE, "r") as f:
        return ujson.load(f)

config = load_config()
wifi_ssid = config["ssid"]
wifi_password = config["password"]
owm_api_key = config["owm_api_key"]


# ========================
# HARDWARE SETUP
# ========================
i2c = I2C(0, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL), freq=400000)
lcd = Lcd_i2c(i2c, I2C_ADDR, 2, 16)


# ========================
# WIFI CONNECTION
# ========================
def connect_wifi():
    lcd.clear()
    lcd.putstr("Connecting to\nWiFi...")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(wifi_ssid, wifi_password)

        timeout = 10
        while timeout > 0:
            if wlan.isconnected():
                break
            timeout -= 1
            utime.sleep(1)

    if wlan.isconnected():
        return True
    else:
        lcd.clear()
        lcd.putstr("WiFi Error!")
        return False


# ========================
# GET LOCATION (IP API)
# ========================
def get_location():
    try:
        res = urequests.get("http://ip-api.com/json/")
        data = res.json()
        res.close()
        return data["lat"], data["lon"]
    except:
        return None


# ========================
# GET WEATHER (OpenWeatherMap)
# ========================
def get_weather(lat, lon):
    url = (
        "http://api.openweathermap.org/data/2.5/weather?"
        "lat={}&lon={}&appid={}&units=metric"
    ).format(lat, lon, owm_api_key)

    try:
        res = urequests.get(url)
        if res.status_code == 200:
            data = res.json()
            res.close()
            return data
        else:
            res.close()
            return None
    except:
        return None


# ========================
# DISPLAY FUNCTIONS
# ========================
def show_coordinates(lat, lon):
    lcd.clear()
    lcd.putstr("Lat:{:.2f}\nLon:{:.2f}".format(lat, lon))
    utime.sleep(5)


def show_weather(weather):
    try:
        temp = weather["main"]["temp"]
        desc = weather["weather"][0]["description"]

        lcd.clear()
        lcd.putstr("{:.1f} C\n{}".format(temp, desc[:16]))
    except:
        lcd.clear()
        lcd.putstr("Data Error")


# ========================
# MAIN PROGRAM LOOP
# ========================
def main():

    while True:

        if not connect_wifi():
            utime.sleep(30)
            continue

        location = get_location()

        if not location:
            lcd.clear()
            lcd.putstr("Location Error")
            utime.sleep(30)
            continue

        lat, lon = location
        show_coordinates(lat, lon)

        # Weather update loop
        while True:

            if not network.WLAN(network.STA_IF).isconnected():
                break  # reconnect

            weather = get_weather(lat, lon)

            if weather:
                show_weather(weather)
            else:
                lcd.clear()
                lcd.putstr("Weather Error")

            # Wait 10 minutes with WiFi check
            for _ in range(WEATHER_UPDATE_INTERVAL):
                if not network.WLAN(network.STA_IF).isconnected():
                    break
                utime.sleep(1)
            else:
                continue

            break  # WiFi lost → reconnect


# ========================
# START PROGRAM
# ========================
if __name__ == "__main__":
    main()