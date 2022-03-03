from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
import random

ua = UserAgent()

def proxyGenerator():
    headers = {'user-agent':ua.random}
    res = requests.get('https://free-proxy-list.net/',headers = headers)
    soup =BeautifulSoup(res.text,'lxml')
    proxies_table = soup.find(id='list')
    proxies = []
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'http': "http://" + row.find_all('td')[0].string +":"+row.find_all('td')[1].string,
            'https':"https://"+row.find_all('td')[0].string + ":" + row.find_all("td")[1].string
        })
    return random.choice(proxies)

option = webdriver.ChromeOptions()
option.add_experimental_option("detach",True)

driver = webdriver.Chrome(options=option)
driver.get('https://www.pixiv.net/ranking.php/') 

# member_button = driver.find_element_by_xpath('/html/body/div[2]/div/section/div[2]/div/a[2]')
# member_button.click()

# acount = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/div[1]/div[1]/input')
# acount.send_keys('jack20499@yahoo.com.tw')

# password = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/div[1]/div[2]/input')
# password.send_keys('7SgfqAPfH3TetuM')

# submit = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/form/button')
# submit.click()

# time.sleep(3)


info = re.findall(r'/artworks/\d*',driver.page_source)
count = 0 
picpath = './data/'
info = info[::2]
for url in info:
    print(url)
    print("http://www.pixiv.net"+url)
    r = requests.get("http://www.pixiv.net"+url)
    u = re.findall(r'https://i.pximg.net/img-original/img.*?g',r.text)
    print(u)
    print(u[0])
    try:
        filename = picpath+"/" + str(count) + ".jpg"       

        headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',            
                   'referer':'http://www.pixiv.net%s' % str(url)
                   }     
        r = requests.get(u[0],headers = headers)        
        with open(filename, 'wb') as f:
            f.write(r.content)
            f.close()
        count += 1
        print('this is '+str(count)+'st img')
                        
        time.sleep(0.2)
    except:
        print('failure')


