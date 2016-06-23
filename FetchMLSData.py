#!/usr/bin/python3.5

import urllib.request
from bs4 import BeautifulSoup
import sys
import re
import csv
import operator
from operator import itemgetter
from re import sub
from decimal import Decimal
import geopy
from geopy.geocoders import Nominatim

with urllib.request.urlopen('http://matrix.abor.com/Matrix/Public/Portal.aspx?ID=0-613312852-10') as response:
   html = response.read()


def cell_text(cell):
    return " ".join(cell.stripped_strings)

def MLSTableRowParser(datalist):
    #Data is presumed to be contained in the list in this format
    #1 - Invalid
    #2 - Invalid
    #3 - Invalid
    #4 - Received
    #5 - Chg Type
    #6 - Invalid
    #7 - Invalid
    #8 - MLS #
    #9 - S
    #10 - Address
    #11 - Bds
    #12 - Fb
    #13 - Hb
    #14 - St
    #15 - Gar
    #16 - Yr Blt
    #17 - Sqft
    #18 - Acres
    #19 - L Price
    #20 - Invalid
    #21 - Type
    #22 - Invalid
    #23 - Invalid
    #24 - Invalid
    #25 - Invalid
    if len(datalist) != 25:
        #print ('Invalid input data: ')
        #print ((datalist)) 
        return None

    dict = {}

    dict['Received'] = datalist[0]
    dict['Chg Type'] = datalist[4]
    dict['MLS'] = datalist[7]
    dict['S'] = datalist[8]
    dict['Address'] = datalist[9]
    dict['Bds'] = datalist[10]
    dict['FB'] = datalist[11]
    dict['HB'] = datalist[12]
    dict['St'] = datalist[13]
    dict['Gar'] = datalist[14]
    dict['Yr Blt'] = datalist[15]
    dict['Sqft'] = datalist[16]
    dict['Acres'] = datalist[17]
    dict['L Price'] = datalist[18]
    dict['Type'] = datalist[20]
    #Derivative data
    price = dict['L Price'].strip('$').replace(',','')
    sqft = dict['Sqft'].replace(',','')
    dict['PricePerSqft'] = int(int(price) / int(sqft))

    if int(dict['Yr Blt']) < 2005:
        return None 

    geolocator = Nominatim()
    location = geolocator.geocode(dict['Address'] + ', Texas')
    print (location.address)

    return dict

soup = BeautifulSoup(html, "lxml")
output = csv.writer(sys.stdout)
HomeList = []

divTag = soup.find_all("div", {"class":"simpleDisplayHeader"})

for tag in divTag:
     for table in tag.find_all('table', {"class":"d1166m2"}):
         for row in table.find_all('tr'):
              col = map(cell_text, row.find_all(re.compile('t[dh]')))
              #output.writerow(col)
              alist = (list(col))
              dict = MLSTableRowParser(alist)
              if dict is not None:
                   HomeList.append(dict)

SortedHomeList = sorted(HomeList, key=operator.itemgetter('PricePerSqft'))

for aHome in SortedHomeList:
    print (aHome)
