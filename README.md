🌦️ MicroPython Weather Station (Pico W)
Tento projekt je jednoduchá meteostanice vytvořená pro platformu Raspberry Pi Pico W. Zařízení se automaticky připojí k WiFi síti, zjistí svou geografickou polohu podle veřejné IP adresy a každých 10 minut stáhne aktuální počasí z API OpenWeatherMap. Výsledná data jsou zobrazena na LCD displeji.

⚙️ Jak program funguje
1️⃣ Po zapnutí zařízení
Na LCD se zobrazí zpráva Connecting to WiFi... a proběhne pokus o připojení k nakonfigurované síti.

2️⃣ Po úspěšném připojení
Program zavolá IP API (ip-api.com) a zjistí zeměpisnou šířku a délku. Tyto souřadnice se na několik sekund zobrazí přímo na displeji pro kontrolu polohy.

3️⃣ Stažení dat
Následně program kontaktuje OpenWeatherMap API, odkud získá:

Aktuální teplotu (°C)

Vlhkost vzduchu (%)

Slovní popis stavu počasí

4️⃣ Automatická smyčka
Každých 10 minut proběhne nová aktualizace. Pokud vypadne WiFi, zařízení se automaticky pokusí znovu připojit. V případě chyby API se na displeji zobrazí varovná hláška.

🗂️ Struktura projektu
main.py – Hlavní spustitelný kód programu.

config.json – Konfidenční soubor (ignorován v .gitignore).

/lib/ – Složka s knihovnami pro hardware.

lcd_api.py – Univerzální rozhraní pro displej.

i2c_lcd.py – Specifický ovladač pro I2C komunikaci.

.gitignore – Definice souborů, které se nenahrávají na GitHub.

README.md – Tato dokumentace.

🔐 Soubor config.json
Soubor obsahuje citlivé údaje a nesmí být nahrán do veřejného repozitáře. Vytvořte jej v kořenovém adresáři se následující strukturou:

JSON
{
    "ssid": "NAZEV_WIFI",
    "password": "HESLO_WIFI",
    "owm_api_key": "VAS_API_KLIC"
}
🌍 Použitá API
IP API (http://ip-api.com/json): Slouží k získání polohy bez nutnosti GPS modulu. Nevyžaduje registraci ani klíč.

OpenWeatherMap API: Slouží ke stažení meteodat. Vyžaduje vlastní API klíč. V rámci bezplatného tarifu je limit cca 1000 požadavků denně.

🖥️ Použitý hardware
Pro projekt je použit mikrokontrolér Raspberry Pi Pico W a standardní I2C LCD displej (16x2).

Zapojení pinů:

SDA propojeno na GP0

SCL propojeno na GP1

VCC propojeno na 5V (VBUS)

GND propojeno na GND

🚀 Nahrání programu
Firmware: Stáhněte a nahrajte MicroPython firmware (UF2 soubor) pro Pico W z oficiálních stránek micropython.org.

Nahrání souborů: Pomocí prostředí Thonny nahrajte soubor main.py, složku /lib a váš vytvořený config.json do paměti zařízení.

Spuštění: Uložte main.py jako hlavní soubor, odpojte a znovu připojte napájení nebo klikněte na "Run" v Thonny.

🛡️ Robustnost programu
Kód je navržen tak, aby byl odolný proti chybám:

Obsahuje mechanismus pro automatické znovupřipojení k WiFi při ztrátě signálu.

Má ošetřené výjimky při komunikaci s webovými servery (timeouty, chybné JSON odpovědi).

Před každou aktualizací dat probíhá kontrola aktivního síťového rozhraní.