# -*- coding: utf-8 -*-

# 高雄市政府 公車資訊

import requests
import xml.sax
import io

busId = list()
busRoute = list()
busStart = list()
busEnd = list()
busData = list()

class KBusHandler(xml.sax.ContentHandler):
    def startElement(self,tag,attr):
        if tag == 'Route':
            busId.append(attr['ID'])
            busRoute.append(attr['nameZh'])
            busStart.append(attr['departureZh'])
            busEnd.append(attr['destinationZh'])

            # print("路線:",attr['nameZh'])
            # print("起站:",attr['departureZh'])
            # print("終站:",attr['destinationZh'])
            # print()


class KBusStop(xml.sax.ContentHandler):
    def startElement(self,tag,attr):
        if tag == 'Stop':
            # print("站牌:",attr['nameZh'])
            if attr['GoBack']== '1': #去程
                print("去程站牌:",attr['nameZh'])
            elif attr['GoBack']== '2': #回程
                print("回程站牌:",attr['nameZh']) 

class KBusId(xml.sax.ContentHandler):
    def startElement(self,tag,attr):
        if tag == 'BusData':
            busData.append(attr['driverid'])
            if attr['GoBack']== '1': #去程
                print("去程公車車牌:",attr['BusID'],"目前車速:",attr['Speed'])
            elif attr['GoBack']== '2': #回程
                print("回程公車車牌:",attr['BusID'],"目前車速:",attr['Speed'])





if __name__ == "__main__":
    
    parser = xml.sax.make_parser() #建立一個解析器
    bus = KBusHandler() #建立一個規則
    parser.setContentHandler(bus) #將規則帶入 解析器

    url = "https://ibus.tbkc.gov.tw/xmlbus/StaticData/GetRoute.xml"
    result = requests.get(url)
    result.encoding = 'utf-8'
    result = result.text

    bObj = io.StringIO(result)

    parser.parse(bObj)

    print(busId)

    bid = input("請輸入路線代號:")
    
    try:
        route = busId.index(bid)
        print("路線名稱:",busRoute[route])
        print("起始站:",busStart[route])
        print("終點站:",busEnd[route])
        print()
    except Exception as err:
        print("錯誤內容：",err)


    routeUrl = "https://ibus.tbkc.gov.tw/xmlbus/StaticData/GetStop.xml"

    #requests 帶參數，參數需用字典方式傳送 https://ibus.tbkc.gov.tw/xmlbus/StaticData/GetStop.xml?routeids=1421

    data = dict()
    data['routeIds'] = bid


    # requests.get 要帶參數時 需用到 params
    result = requests.get(routeUrl,params=data)
    result.encoding = "utf-8"
    result = result.text

    stop = KBusStop()#建立一個規則
    parser.setContentHandler(stop) #將規則帶入 解析器
    sObj = io.StringIO(result)
    parser.parse(sObj)

    print()

    # 顯示目前所選的路線即時公車車牌 (Assignment)

    routeUrl = "https://ibus.tbkc.gov.tw/xmlbus/GetBusData.xml"

    #requests 帶參數，參數需用字典方式傳送 https://ibus.tbkc.gov.tw/xmlbus/GetBusData.xml?routeids=1421

    data = dict()
    data['routeIds'] = bid


    # requests.get 要帶參數時 需用到 params
    result = requests.get(routeUrl,params=data)
    result.encoding = "utf-8"
    result = result.text

    busId = KBusId()#建立一個規則
    parser.setContentHandler(busId) #將規則帶入 解析器
    sObj = io.StringIO(result)
    parser.parse(sObj)

    if len(busData)==0:
        print("路線{} 無公車在路上行駛中...".format(bid))
    else:
        print("路線{} 有{}台公車 在路上行駛中".format(bid,len(busData)))    











