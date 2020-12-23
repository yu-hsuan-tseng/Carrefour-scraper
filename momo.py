'''
    Momo shopping data crawling
'''
import pandas as pd 
import numpy as np 
from bs4 import BeautifulSoup 
import urllib.request as req
import requests
from selenium import webdriver
from tqdm import tqdm 
from time import sleep
from datetime import date
import time
import ssl





def get_category(url):
    
    dt = date.today() 
    dt = dt.strftime('%Y%m%d')   
    df = {'L1':[],'L2':[],'L3':[],'L3 link':[]}
    #browser = webdriver.Chrome(executable_path="./chromedriver")
    #browser.get(url)
    #headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    opener = req.build_opener()
    opener.addheaders = [{'User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}]
    req.install_opener(opener)
    response =  req.urlopen(url)
    r = response.read().decode('utf-8')
    soup = BeautifulSoup(r,'html.parser')
    #tag = soup.find_all("div",class_="btclass navcontent_innerwarp category2019")
    all_l1 = soup.find("ul",class_="navcontent_listul").find_all('li')
    l1 = []
    tag = soup.find_all("div",class_="btclass navcontent_innerwarp category2019")
    for i in all_l1:
        l1.append(i.text)
    for l,t in zip(l1,tag):
        l2 = t.find_all("td")
        for i in l2:
            
            all_l3 = i.find_all("a",href=True)
            for k in all_l3:
                df['L1'].append(l)
                df['L2'].append(i.find("p",class_="groupName").text)
                df['L3'].append(k.text)
                df['L3 link'].append(k['href'])


        
    
    #browser.quit()
    df = pd.DataFrame(df)
    df.index = np.arange(1,len(df)+1)
    df.to_csv(dt+"_momo_category.csv",index=False)
    df.to_excel(dt+"_momo_category.xlsx",index=False,engine='xlsxwriter')
    return df 



def get_product_links(urls):
    #headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    links = []
    for url in tqdm(urls):
        try:
            opener = req.build_opener()
            opener.addheaders = [{'User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}]
            req.install_opener(opener)
            response =  req.urlopen(url)
            r = response.read().decode('utf-8')
            soup = BeautifulSoup(r,'html.parser')
            tag = soup.find("div",class_='contentArea BTDME CLCODE').find_all('a',href=True)
            for t in tag:
                links.append("https://www.momoshop.com.tw"+t['href'])
        except:
            time.sleep(1)
            pass
    return links

def get_info(urls):
    df = {"product":[],"product url":[],"image url":[],"product number":[],"suggested price":[],"price":[],"sales":[],"specification":[],"category 1":[],"category 2":[],"category 3":[],"category 4":[],"category 5":[]}
    #headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    p_urls = []
    for url in tqdm(urls):
        try:
            opener = req.build_opener()
            opener.addheaders = [{'User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}]
            req.install_opener(opener)
            response =  req.urlopen(url)
            r = response.read().decode('utf-8')
            soup = BeautifulSoup(r,'html.parser')
            tag = soup.find("div",class_="contentArea").find_all("li")
            for t in tag:
                try:
                    p_urls.append("https://www.momoshop.com.tw"+t.find_all("a",href=True)[0]['href'])
                except:
                    pass
        except:
            time.sleep(1)
            pass
    for url in tqdm(p_urls[:10]):
        
        opener = req.build_opener()
        opener.addheaders = [{'User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}]
        req.install_opener(opener)
        response =  req.urlopen(url)
        r = response.read().decode('utf-8')
        soup = BeautifulSoup(r,'html.parser')
        df['product url'].append(url)
        try:
            df['product'].append(soup.find("div",class_="prdwarp").find_all("h3")[0].text)
        except:
            df['product'].append("None")
        
        try:
            df['image url'].append(soup.find("div",class_="prdimgArea").find_all('img')[0]['src'])
        except:
            df['image url'].append("None")

        try:
            df['product number'].append(soup.find("li",class_="fast").find_all('br')[0].text.replace("品號：",""))
        except:
            df['product number'].append("None")

        try:
            df['suggested price'].append(soup.find("ul",class_="prdPrice").find_all("li")[0].text)
        except:
            df['suggested price'].append("None")
        
        try:
            df['price'].append(soup.find("ul",class_="prdPrice").find("li",class_="special").text[1])
        except:
            df['price'].append("None")
        
        try:
            df['sales'].append(soup.find("ul",class_="ineventArea").find_all('a')[0].text)
        except:
            df['sales'].append("None")

        try:
            df['specification'].append(soup.find("ul",class_="categoryActivityInfo gmclass").find_all("li")[1:].text)
        except:
            df['specification'].append("None")

        # category
        cate = soup.find("div",class_=" bt770class").find_all("a",href=True)
        try:
            df['category 1'].append(cate[0].text)
        except:
            df['category 1'].append("None")
        try:
            df['category 2'].append(cate[1].text)
        except:
            df['category 2'].append("None")
        try:
            df['category 3'].append(cate[2].text)
        except:
            df['category 3'].append("None")
        try:
            df['category 4'].append(cate[3].text)
        except:
            df['category 4'].append("None")
        try:
            df['category 5'].append(cate[4].text)
        except:
            df['category 5'].append("None")

    #df = pd.DataFrame(df)
    #df.index = np.arange(1,len(df)+1)
    return df


if __name__=="__main__":


    url = "https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1912900000&mdiv=1099600000-bt_0_996_10-&ctype=B"
    ssl._create_default_https_context = ssl._create_unverified_context
    df = get_category(url)
    links = get_product_links(df['L3 link'])
    print(len(links))
    df = get_info(links)
    print(df)