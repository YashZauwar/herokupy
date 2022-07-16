#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
import pandas as pd
import ipywidgets as widgets

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
        'accept-encoding': 'gzip, deflate, br'}
sess = requests.Session()
cookies = dict()

def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)

def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==401):
        set_cookie()
        response = sess.get(url_nf, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==200):
        return response.text
    return ""

stockselect = widgets.Dropdown(
    options=['TATAMOTORS', 'RELIANCE', 'INFOSYS','MARUTI','HUL','ITC','TCS','ADANIENT','ADANIPORT'],
    #value='RELIANCE',
    description='Select Stock:',
    disabled=False,
)

display(stockselect)

reset_button = widgets.Button(description = 'Reset Data')

button2 = widgets.Button(description = 'Fetch Option Chain Data')

def reset():
    with out:
        clear_output()
    
def fetch_oi(expiry_dt):
    b = stockselect.value
    new_url = "https://www.nseindia.com/api/option-chain-equities?symbol="+b
    print(b)
    print(new_url)
    response_text = get_data(new_url)
    dajs = json.loads(response_text)
    expiry_dt = dajs["records"]["expiryDates"][0]

    ce_values = [data['CE'] for data in dajs['records']['data'] if "CE" in data and data['expiryDate'] == expiry_dt]
    pe_values = [data['PE'] for data in dajs['records']['data'] if "PE" in data and data['expiryDate'] == expiry_dt]

    ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])
    pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])

    print(strPurple((ce_dt[['strikePrice','lastPrice','impliedVolatility']])))
    print(pe_dt[['strikePrice','lastPrice','impliedVolatility']])
    
display(button2)
button2.on_click(fetch_oi)

display(reset_button)
reset_button.on_click(reset)

