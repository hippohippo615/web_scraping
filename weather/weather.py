import requests
import json
import urllib3


'''
案例：鄉鎮天氣預報-臺中市未來3天天氣預報

說明頁面: https://opendata.cwa.gov.tw/dataset/all/F-D0047-073
'''

# 忽略 InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AUTH_CODE    = "授權碼"
API_URL_TMPL = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-D0047-073" \
               "?Authorization={auth}&downloadType=WEB&format=JSON"

def fetch_weather_json(auth_code: str) -> dict:
    """向中央氣象局 API 取得 JSON，回傳解析後的 dict"""
    url = API_URL_TMPL.format(auth=auth_code)
    try:  # 簡單用法：連線+讀取都最多等 10 秒
        resp = requests.get(url, verify=False, timeout=10)
        resp.raise_for_status()
        return resp.json()  #data2 = json.loads(resp.text)
    except requests.RequestException as e:
        print(f"❌ 取得天氣資料失敗：{e}")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失敗：{e}")
        raise

def extract_locations(data: dict) -> dict:
    """從 API 回傳資料中取出 Locations 區段"""
    try:
        return data["cwaopendata"]["Dataset"]["Locations"]
    except KeyError as e:
        print(f"❌ 資料格式錯誤，找不到欄位：{e}")
        raise

def print_location_names(locations: dict):
    """列出縣市及其所有鄉鎮名稱"""
    print(f"縣市名稱: {locations.get('LocationsName', '未知')}")
    for loc in locations.get("Location", []):
        name = loc.get("LocationName", "")
        print(f"  鄉鎮名稱: {name}")

def print_noon_temperatures(locations: dict):
    """只印出未來 3 天中，12:00:00+08:00 時段的溫度"""
    for loc in locations.get("Location", []):
        name = loc.get("LocationName", "")
        print(f"\n=== 區域：{name} ===")
        for elem in loc.get("WeatherElement", []):
            if elem.get("ElementName") == "溫度":
                for period in elem.get("Time", []):
                    dt = period.get("DataTime", "")
                    if dt.endswith("12:00:00+08:00"):
                        temp = period.get("ElementValue", {}).get("Temperature", "N/A")
                        print(f"{dt} → 溫度：{temp}°C")

def main():
    data      = fetch_weather_json(AUTH_CODE)
    locations = extract_locations(data)
    print_location_names(locations)
    print_noon_temperatures(locations)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[FATAL] 程式異常結束：{e}")