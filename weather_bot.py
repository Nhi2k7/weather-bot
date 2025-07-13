import requests
from datetime import datetime

# ========== CẤU HÌNH ==========
BOT_TOKEN = "7633829216:AAHqBIB3ib-2sv36NTL6daU34LOj45jjsZ0"
CHAT_ID = "7496729232"
API_KEY = "58948bab54ea52bb8c42c8b9a6d76d1f"
UNITS = "metric"
LANG = "vi"

# ========== DANH SÁCH VỊ TRÍ ==========
locations = [
    {"name": "Mỹ Tho", "lat": 10.306403, "lon": 106.223740},
    {"name": "Cẩm Phả", "lat": 21.035063, "lon": 107.252755}
]

# ========== GỬI TELEGRAM ==========
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("⚠️ Lỗi gửi Telegram:", e)

# ========== LẤY DỮ LIỆU HIỆN TẠI ==========
def get_weather(lat, lon, name):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={UNITS}&lang={LANG}"
    try:
        res = requests.get(url).json()
        if res.get("cod") != 200:
            return f"❌ Không lấy được thời tiết tại {name}.\n"

        temp = res["main"]["temp"]
        feels_like = res["main"]["feels_like"]
        desc = res["weather"][0]["description"].capitalize()
        humidity = res["main"]["humidity"]
        wind = res["wind"]["speed"]
        rain_alert = "☔ *Có thể có mưa!*" if "rain" in res else ""

        msg = f"\n📍 *{name}*\n" \
              f"🌡 {temp}°C (Cảm giác: {feels_like}°C)\n" \
              f"💧 Độ ẩm: {humidity}%  💨 Gió: {wind} m/s\n" \
              f"☁️ Trạng thái: {desc}\n" + (f"{rain_alert}\n" if rain_alert else "")
        return msg
    except Exception as e:
        return f"⚠️ Lỗi lấy thời tiết tại {name}: {e}"

# ========== DỰ BÁO ==========
def get_forecast(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units={UNITS}&lang={LANG}"
    try:
        res = requests.get(url).json()
        if res.get("cod") != "200":
            return ""

        msg = "\n📅 *Dự báo 15 giờ tới:*\n"
        for i in res["list"][:5]:
            time = datetime.fromtimestamp(i["dt"]).strftime("%H:%M %d/%m")
            temp = i["main"]["temp"]
            desc = i["weather"][0]["description"].capitalize()
            rain = "☔" if "rain" in i else ""
            msg += f"- {time}: {temp}°C, {desc} {rain}\n"
        return msg
    except Exception as e:
        return ""

# ========== LINK RADAR ==========
def radar_link(lat, lon):
    lat = round(lat, 2)
    lon = round(lon, 2)
    return f"[Xem radar mưa](https://embed.windy.com/embed2.html?lat={lat}&lon={lon}&detailLat={lat}&detailLon={lon}&width=650&height=450&zoom=8)"

# ========== MAIN ==========
def main():
    message = "🌦 *Bản tin thời tiết tự động:*\n\n"
    for loc in locations:
        current = get_weather(loc["lat"], loc["lon"], loc["name"])
        forecast = get_forecast(loc["lat"], loc["lon"])
        radar = radar_link(loc["lat"], loc["lon"])

        message += current
        message += forecast
        message += "\n🛰 " + radar + "\n\n" + "-"*20 + "\n"

    send_telegram(message)

if __name__ == "__main__":
    main()
