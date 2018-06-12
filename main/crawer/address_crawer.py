import uuid

import requests
from bs4 import BeautifulSoup

# 地址类型
from main.models.address import Address


class AddressType:
    def __init__(self):
        self.type = ''
        self.url = ''

# 获取地址类型
def get_address_type_url(url):
    address_type_list = []
    try:
        data = requests.get(url).text
        xml_data = BeautifulSoup(data, "lxml")
        address_type_content = xml_data.select(".sortBox a")
        for item in address_type_content:
            address_type = AddressType()
            address_type.type = item.get_text()
            address_type.url = item.get('href')
            address_type_list.append(address_type)
    except Exception as ex:
        print(ex)
    finally:
        return address_type_list

# 获取某个类型下所有地名
def get_address_name(url):
    try:
        data = requests.get(url).text
        xml_data = BeautifulSoup(data, "lxml")
        address_content = xml_data.select(".sortC a")
        for item in address_content:
            address_obj = Address(address_id=uuid.uuid1(),name=item.get_text(),url=item.get('href'))
            address_obj.save()
            print(item.get_text())
    except Exception as ex:
        print(ex)

def get_address_by_crawer():
    address_type = get_address_type_url('http://poi.mapbar.com/lijiang/980/')
    for item in address_type:
        print(item.type,item.url)
        get_address_name(item.url)