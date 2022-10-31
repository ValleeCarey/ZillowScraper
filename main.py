import os
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import regex as re
import requests
import PyQuery as pq

pd.set_option('display.max_rows', None)
pd.set_option('mode.chained_assignment',None)

headers = {
    'authority': 'www.zillow.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    # Requests sorts cookies= alphabetically
    # 'cookie': f"JSESSIONID=324C61E9C0C1AA25E9A40BB70768FDBF; zguid=24|%24f393b65a-45b0-40ca-a30f-04bb7de1cd13; zgsession=1|55a5e89d-fef9-421f-931f-34fab9983db4; _ga=GA1.2.1432972542.1667223859; _gid=GA1.2.2047347711.1667223859; zjs_user_id=null; zg_anonymous_id=%22dd54b92e-c5db-4abd-b5f8-31053d2ed084%22; zjs_anonymous_id=%22f393b65a-45b0-40ca-a30f-04bb7de1cd13%22; pxcts=1ec69583-5922-11ed-bbbd-4b626a466571; _pxvid=1ec684cd-5922-11ed-bbbd-4b626a466571; _gcl_au=1.1.1849360235.1667223861; KruxPixel=true; DoubleClickSession=true; __gads=ID=2fe51cc21f53e3c7:T=1667223860:S=ALNI_MbF1zbwT5Q6YEq-qVISI4K6KZ7XrA; __gpi=UID=000008eb6918fa8e:T=1667223860:RT=1667223860:S=ALNI_MadGrSNNX1xRt5tjnifQmAiyokRGg; __pdst=a65a0ff56f4b40fbbd482a1a1cee1d74; _fbp=fb.1.1667223861333.342845985; _pin_unauth=dWlkPU5HTXdNRGsyTmpNdE1URm1NeTAwTTJJMUxXSTFOR010TkdWak9ETmtObVk0TjJRMA; _clck=1trnaqc|1|f66|0; KruxAddition=true; utag_main=v_id:01842e493821001696117ec61e8505075020f06d00998{_sn:1$_se:1$_ss:1$_st:1667225661281$ses_id:1667223861281%3Bexp-session$_pn:1%3Bexp-session$dcsyncran:1%3Bexp-session$tdsyncran:1%3Bexp-session$dc_visit:1$dc_event:1%3Bexp-session$dc_region:us-east-1%3Bexp-session$ttd_uuid:01d0a217-2621-4673-850d-94786849ac70%3Bexp-session;} _px3=7ba7554c24fa1dce1a34aec730421a6faf3ca2522e9fa203c92fa2ca55bba6ff:8/GIhmq7i4BmpNJeljNawL+gbrCmrDvSrkzPv44nfEZgQ7iAP2qMN0Mc40naAt/1if6w61mQmikv2kzOzfGaIA==:1000:GYoJwCTySvGRznaUw6vyJ5m3+s6btAGmC/F6ZhIHj03+vWH+r7keAlno23GcW5lJzXnWQ6l0On7mbUAVTD9aUZH2zRT+oVZf0je+OHJHIDmUSeqcgaguoXEK4bFwrS9cZKthIfVfHFa9RwTLA8B0lB4oMFFPf9u2d/rTd9vZPAlY9EOTtuBCWc8HraOVeX/tHCqJLZZl0n1erq84KBh3SA==; _uetsid=1f92ff40592211eda1398b9425c5dff6; _uetvid=2b5c91a037c111eda88a89617fd84db2; _gat=1; _clsk=1hicaz3|1667223986239|15|0|m.clarity.ms/collect; AWSALB=LUNHlxLowksJu29I8uTJgKCU60S4eu80rl9ujmHCmIqPHzvnQvQ5A7OAipsujs4Y9W7J33/7blPzxgZZGbSE1OklxBwo2e2OA6tyUq7ou2x1xxJ6cGS3fnaGVyxw; AWSALBCORS=LUNHlxLowksJu29I8uTJgKCU60S4eu80rl9ujmHCmIqPHzvnQvQ5A7OAipsujs4Y9W7J33/7blPzxgZZGbSE1OklxBwo2e2OA6tyUq7ou2x1xxJ6cGS3fnaGVyxw; search=6|1669815985955%7Crect%3D36.94978880929768%252C-85.7360511640625%252C35.43819056243306%252C-87.8344398359375%26rid%3D6118%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%096118%09%09%09%09%09%09",
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

response = requests.get('https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A36.94978880929768%2C%22east%22%3A-85.7360511640625%2C%22south%22%3A35.43819056243306%2C%22west%22%3A-87.8344398359375%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6118%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%2C%22sortSelection%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A9%7D&wants=\\{%22cat1%22:\\[%22listResults%22\\],%22cat2%22:\\[%22total%22\\]\\}&requestId=8', headers=headers)

with requests.session() as s:
    city = 'Nashville'
    page = 1
    end = 5
    url = ''
    url_list = []

    while page <= end:
        url = 'https://www.zillow.com/homes/for_sale/' + city + f'{page}_p'
        url_list.append(url)
        page += 1

        request = ''
        request_list = []

        for url in url_list:
            request = s.get(url, headers=headers)
            request_list.append(request)

    soup = ''
    soup_list = []

    for request in request_list:
        soup = BeautifulSoup(request.content, 'html.parser')
        soup_list.append(soup)

    df_list = []
    for soup in soup_list:
        df = pd.DataFrame()
        for i in soup:
            address = soup.find_all(class_='list-card-addr')
            price = list(soup.find_all(class_='list-card-price'))
            beds = list(soup.find_all("ul", class_="list-card-details"))
            details = soup.find_all('div', {'class': 'list-card-details'})
            home_type = soup.find_all('div', {'class': 'list-card-footer'})
            last_updated = soup.find_all('div', {'class': 'list-card-top'})
            brokerage = list(soup.find_all(class_='list-card-brokerage list-card-img-overlay', text=True))
            link = soup.find_all(class_='list-card-link')

            df['prices'] = price
            df['address'] = address
            df['beds'] = beds
        urls = []

        for link in soup.find_all("article"):
            href = link.find('a', class_="list-card-link")
            addresses = href.find('address')
            addresses.extract()
            urls.append(href)

        df['links'] = urls
        df['links'] = df['links'].astype('str')
        df['links'] = df['links'].replace('<a class = "list-card-link-card-link-top-margin" href="',' ',regex=True)
        df['links'] = df['links'].replace('" tabindex="0">', ' ',regex=True)
        df_list.append(df)


    df = pd.concat(df_list).reset_index().drop(columns='index')

    # remove html tags
    # df['prices'] = df['prices'].replace('\[', '', regex=True)
    df.loc[:, 'address'] = df.loc[:, 'address'].replace('', '', regex=True)
    # df['prices'] = df['prices'].replace('\]', '', regex=True)
    df.loc[:, 'address'] = df.loc[:, 'address'].replace('', '', regex=True)
    # df['prices'] = df['prices'].str.replace(r'\D', '')

    # filter unwanted property types
    df = df[~df['beds'].str.contains("Land for sale")]

    # remove html tags from beds column
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace('
                                                  '
                                                  , ' ', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace(' bds
                                                  '
                                                  , ' ', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace(' ba
                                                  '
                                                  , ' ', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace(' bd
                                                  '
                                                  , ' ', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace('- Foreclosure', '- Foreclosure', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace(' sqft
                                                  '
                                                  , ' ', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace(' acres lot
                                                  '
                                                  , ' ', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace('', '', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace('--', '0', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace('Multi-family', 'Multifamily', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace(' for sale', '', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace('- <!0 0>Auction', '- Auction', regex=True)
    df.loc[:, 'beds'] = df.loc[:, 'beds'].replace('- <!0 0>Pending', '- Pending', regex=True)
