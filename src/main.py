import network
import urequests
import utime
import ujson
from lcd import Lcd_i2c
from machine import Pin
# Importujte ovladač pro váš LCD (např. pico_i2c_lcd)
# z dokumentace k vašemu konkrétnímu displeji

## --- NASTAVENÍ ---
I2C_ADDR = 0x27  # Obvyklá adresa pro I2C LCD
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
# lcd = I2cLcd(i2c, I2C_ADDR, 2, 16) # Inicializace vašeho LCD

def load_config():
    with open('config.json', 'r') as f:
        return ujson.load(f)

config = load_config()

## --- FUNKCE ---

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        # lcd.putstr("Connecting to\nWiFi...")
        wlan.connect(config['ssid'], config['password'])
        
        # Timeout pro připojení (cca 10s)
        attempt = 0
        while not wlan.isconnected() and attempt < 10:
            utime.sleep(1)
            attempt += 1
            
    if wlan.isconnected():
        print("Connected!", wlan.ifconfig())
        return True
    return False

def get_location():
    try:
        res = urequests.get("http://ip-api.com/json/")
        data = res.json()
        res.close()
        return data['lat'], data['lon'], data['city']
    except Exception as e:
        print("IP API Error:", e)
        return None

def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric".format(lat, lon, config['owm_api_key'])
    try:
        res = urequests.get(url)
        if res.status_code == 200:
            data = res.json()
            res.close()
            return data
        else:
            print("Weather API Status:", res.status_code)
            res.close()
            return None
    except Exception as e:
        print("Weather API Error:", e)
        return None

## --- HLAVNÍ SMYČKA ---

def main():
    while True:
        if not connect_wifi():
            # lcd.clear()
            # lcd.putstr("WiFi Error!")
            utime.sleep(30)
            continue

        # Získání polohy
        loc = get_location()
        if loc:
            lat, lon, city = loc
            # lcd.clear()
            # lcd.putstr("Loc: {},{}\nCity: {}".format(lat, lon, city))
            utime.sleep(5) # Zobrazení souřadnic na pár sekund
            
            while True: # Smyčka pro aktualizaci počasí
                print("Updating weather...")
                weather = get_weather(lat, lon)
                
                if weather:
                    temp = weather['main']['temp']
                    desc = weather['weather'][0]['description']
                    # lcd.clear()
                    # lcd.putstr("Temp: {:.1f} C\n{}".format(temp, desc))
                else:
                    # lcd.clear()
                    # lcd.putstr("API Data Error")
                
                # Čekání 10 minut (600 s), ale s kontrolou WiFi
                for _ in range(600):
                    if not network.WLAN(network.STA_IF).isconnected():
                        break # Vyskočí do vnější smyčky pro znovupřipojení
                    utime.sleep(1)
                else:
                    continue # Pokračuje vnitřní smyčka (weather update)
                break # Pokud selhala WiFi, rozbije vnitřní smyčku

if __name__ == "__main__":
    main()