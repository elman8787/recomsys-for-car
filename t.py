import arabic_reshaper
import requests
from bs4 import BeautifulSoup as bf
from bidi.algorithm import get_display
import arabic_reshaper
import pandas as pd
import numpy as np
from tabulate import tabulate
import re

def convert(text):
    reshaped_text = arabic_reshaper.reshape(text)
    converted = get_display(reshaped_text)
    return converted

r = requests.get('https://www.hamrah-mechanic.com/carprice')
soup = bf(r.text , 'html.parser')
print(soup)
name = soup.find_all('div' , attrs={'class':'carsBrandPriceList_model__name__fYre5'})
price = soup.find_all('div' , attrs={'class':'carsBrandPriceList_price__number__APBu0'})
year = soup.find_all('div',attrs={'class':'carsBrandPriceList_model__type__1L_I7'})
nameData,priceData,yearData,modelData = [],[],[],[]
for n in name:
    nameData.append(convert(n.text.strip()))
for p in price:
    priceData.append(p.text.strip())
for y in year:
    y = y.text
    digit = re.findall(r'\d+',y)
    for d in range(0,len(digit)):
        digit[d] = int(digit[d])
    for k in digit:
        if k<=1000 or k>=3000:
            digit.remove(k)
    for l in digit:
        if l>=1000 and l<=2000:
            if l>1401 or l<1380:
                digit.remove(l)
        if l>=2000 and l<=3000:
            if l>2022:
                digit.remove(l)
    yearData.append(digit)
d = {'name':nameData,'price':priceData,'year':yearData}
df = pd.DataFrame(d)
for q in range(0,len(df['year'])):
    df['year'][q] = df['year'][q][0]
for w in range(0,len(df['price'])):
    t = 0
    for r in df['price'][w]:
        if r==',':
            t+=1
    df['price'][w] = int(df['price'][w].replace(',','',t))
#df.to_excel('data.xlsx')