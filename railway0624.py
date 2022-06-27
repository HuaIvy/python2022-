# -*- coding: utf-8 -*-

# post  header param 

import requests
from bs4 import BeautifulSoup

# post 台鐵時刻表  依車站 網站轉址 F12 檢視 Network
url = "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybystation" 

# https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime  ↓
# https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybystation (post)

# User-Agent 可寫大寫 亦可小寫
header = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'

}

param = {
   '_csrf': '75fd8ac0-35e5-460b-b5ff-8761dd5c8931',
'rideDate': '2022/06/27',
'station': '4340-新左營'

}


station = requests.post(url,data=param,headers=header).text

soup = BeautifulSoup(station,'html.parser')

content = soup.find('tbody')

table = content.find_all('tr')


for row in table:
    rail = row.find_all('td')
    if not (rail==None):
        if len(rail)>0:
            car = rail[0].text.strip().replace('(','')
            car = car.replace(')','')
            goTo = car.split('→')
            print("車種車次:",goTo[0].strip(),'->',goTo[1].strip())
            print("出發時間:",rail[1].text.strip())
            print("終點站:",rail[2].text.strip())
            print("服務設施:",rail[3].text.strip())
            print("狀態:",rail[4].text.strip())
            print()


               
