import requests, json
import urllib3

'''
案例：鄉鎮天氣預報-臺中市未來3天天氣預報

說明頁面: https://opendata.cwa.gov.tw/dataset/all/F-D0047-073
'''

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 授權碼  

auth_code = "授權碼"
response = requests.get(
    f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-D0047-073?Authorization={auth_code}&downloadType=WEB&format=JSON",
    verify=False  # 忽略憑證驗證
)

# 將 json 轉成物件
obj = json.loads(response.text)

#列出縣市名稱
locations = obj["cwaopendata"]["Dataset"]["Locations"]
print(f"縣市名稱: {locations['LocationsName']}")




for loc in locations["Location"]:
    print(f"  鄉鎮名稱: {loc['LocationName']}")



#印出每一區
for objLocation in obj["cwaopendata"]["Dataset"]["Locations"]["Location"]:
          print(f"  鄉鎮名稱: {objLocation['LocationName']}")

#print()

# 印出每一個區的一週天氣的溫度
for objLocation in obj["cwaopendata"]["Dataset"]["Locations"]["Location"]:
    print()
    print(f"=== 區域名稱: {objLocation['LocationName']} ===")
    print()
    for objWeatherElement in objLocation["WeatherElement"]:
        if objWeatherElement['ElementName'] == '溫度':
            for objTime in objWeatherElement['Time']:
                if objTime['DataTime'].endswith("12:00:00+08:00"):
                    print(f"{objTime['DataTime']} → 溫度：{objTime ['ElementValue']['Temperature']}°C")
                
   #         for objTime in objWeatherElement["time"]:
    #            print(f"開始時間: {objTime['startTime']}, 結束時間: {objTime['endTime']}")
     #           print(f"溫度: {objTime['elementValue']['measures']} {objTime['elementValue']['value']}")
      #          print()