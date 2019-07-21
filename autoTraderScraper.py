#!/usr/bin/python3.7

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen

#pd.set_option('display.width', 1000)
#pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

names = []
prices = []
year = []
body_type = []
milage = []
engine = []
hp = []
transmission = []
petrol_type = []

print(' *  *  *  *  *  *  *')
#Search Autotrader. Copy result url into sitesearch.
sitesearch = "https://www.autotrader.co.uk/car-search?sort=sponsored&radius=1500&postcode=bt324gy&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&make=BMW&model=5%20SERIES&aggregatedTrim=535d"

html = urlopen(sitesearch)
html_soup = BeautifulSoup(html, 'html.parser')

pages = html_soup.find_all('li',class_ = 'pagination--li')
#print(len(pages))
pagecount = len(pages)-2 # Need to check this assumption holds true.
#print("Pages =", pagecount)

page =1
while page <= pagecount:
    sitePage = sitesearch+'&page='+str(page)
    print('Page ',page, ' of ', pagecount)
    html = urlopen(sitePage)
    html_soup = BeautifulSoup(html, 'html.parser')
    page +=1

    outer = html_soup.find_all('article',class_ = "sso-listing")
    print('Outer count = ', len(outer))
    print('')

    for inner in outer:
        lis = []
        names.append(inner.find_all('a', class_ = "js-click-handler")[1].text)
        prices.append(inner.find('div', class_='vehicle-price').text)
        for li in inner.find_all('ul', class_='listing-key-specs'):
            for i in li.find_all('li')[-7:]:
                lis.append(i.text)
        year.append(lis[0])
        body_type.append(lis[1])
        milage.append(lis[2])
        engine.append(lis[3])
        hp.append(lis[4])
        transmission.append(lis[5])
        petrol_type.append(lis[6])

test_df = pd.DataFrame.from_dict({'Title': names, 'Price': prices, 'Year': year, 'Body Type': body_type, 'Mileage': milage, 'Engine Size': engine, 'HP': hp, 'Transmission': transmission, 'Petrol Type': petrol_type}, orient='index')
print(test_df.transpose())
print()

(test_df.transpose()).to_csv('Scrape535.csv', encoding='utf-8', index=False)

#toDo
#1.extend table to include other key info.
# e.g. optional extras - freetext so will be inconsistent.
