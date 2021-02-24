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
                if "https" in t['href']:
                    links.append(t['href'])
                else:
                    links.append("https://www.momoshop.com.tw"+t['href'])
        except:
            time.sleep(1)
            pass
    return links

def get_info(urls):
    df = {"product":[],"product url":[],"image url":[],"product number":[],"suggested price":[],"price":[],"sales":[],"description":[],"detailed specification":[],"specification":[],"category 1":[],"category 2":[],"category 3":[],"category 4":[],"category 5":[]}
    #headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    p_urls = []
    browser = webdriver.Chrome(executable_path="./chromedriver")
    for url in tqdm(urls[:5000]):
        try:
            '''
            opener = req.build_opener()
            opener.addheaders = [{'User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}]
            req.install_opener(opener)
            response =  req.urlopen(url)
            r = response.read().decode('utf-8')
            '''
            browser.get(url)
            soup = BeautifulSoup(browser.page_source,'html.parser')
            tag = soup.find("div",class_="prdListArea bt770class").find_all("li",class_="eachGood")
            for t in tag:
                try:    
                    if "https" in t.find_all("a",class_="prdUrl")[0]['href']:
                        p_urls.append(t.find_all("a",class_="prdUrl")[0]['href'])
                    else:
                        p_urls.append("https://www.momoshop.com.tw"+t.find_all("a",class_="prdUrl")[0]['href'])
                except:
                    pass
        except:
            time.sleep(1)
            pass
    #browser.quit()
    print("product links :"+str(len(p_urls)))
    for url in tqdm(p_urls[:5870]):
        try:
            '''
            opener = req.build_opener()
            opener.addheaders = [{'User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}]
            req.install_opener(opener)
            response =  req.urlopen(url)
            r = response.read().decode('utf-8')
            '''
            browser.get(url)
            soup = BeautifulSoup(browser.page_source,'html.parser')
            p_n = soup.find("div",class_="prdwarp").find_all("h3")[0].text
            
            try:
                df['product'].append(soup.find("div",class_="prdwarp").find_all("h3")[0].text)
            except:
                df['product'].append("")
            
            try:
                if "https" in soup.find("div",class_="prdimgArea").find_all('img')[0]['src']:
                    df['image url'].append(soup.find("div",class_="prdimgArea").find_all('img')[0]['src'])
                elif "//" in soup.find("div",class_="prdimgArea").find_all('img')[0]['src']:
                    df['image url'].append("https:"+soup.find("div",class_="prdimgArea").find_all('img')[0]['src'])
                else:
                    u = "https://img3.momoshop.com.tw"+soup.find("div",class_="prdimgArea").find_all('img')[0]['src']
                    df['image url'].append(u.replace("..",""))
            except:
                df['image url'].append("")

            try:
                df['product number'].append(soup.find("li",class_="fast").find_('a').text.replace("品號：",""))
            except:
                
                df['product number'].append("")

            try:
                df['suggested price'].append(soup.find("ul",class_="prdPrice").find_all("del").text)
            except:
                try:
                    df['suggested price'].append(soup.find("ul",class_="prdPrice").find("li",class_="special").find("span").text)
                except:
                    df['suggested price'].append("")
            
            try:
                df['price'].append(soup.find("ul",class_="prdPrice").find("li",class_="special").find("span").text)
            except:
                df['price'].append("")
            
            try:
                df['sales'].append(soup.find("ul",class_="ineventArea").find_all('a')[0].text)
            except:
                df['sales'].append("")

            try:
                df['specification'].append(soup.find("ul",class_="categoryActivityInfo gmclass").find_all("li")[1:].text)
            except:
                df['specification'].append("")

            # category
            
            try:
                cate = soup.find("div",class_="bt770class").find_all("li")
                df['category 1'].append(cate[0].text)
            except:
                df['category 1'].append("")
            try:
                df['category 2'].append(cate[1].text)
            except:
                df['category 2'].append("")
            try:
                df['category 3'].append(cate[2].text)
            except:
                df['category 3'].append("")
            try:
                df['category 4'].append(cate[3].text)
            except:
                df['category 4'].append("")
            try:
                df['category 5'].append(cate[4].text)
            except:
                df['category 5'].append("")
            try:
                df['detailed specification'].append(soup.find("div",class_="attributesListArea").text)
            except:
                df['detailed specification'].append("")
            df['product url'].append(url)
            df['description'].append("")
        except:
            pass
    try:
        browser.quit()
    except:
        pass
    df = pd.DataFrame(df)
    df.index = np.arange(1,len(df)+1)
    df = df.drop_duplicates()
    return df

def main():


    url = "https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=4199900000&mdiv=1099700000-bt_0_957_01-&ctype=B"
    ssl._create_default_https_context = ssl._create_unverified_context
    
    df = get_category(url)
   
    #df = pd.read_csv("20210118_MOMO_Category.csv")
    links = get_product_links(df['L3 link'])
    print(len(links))
    df = get_info(links)
    dt = date.today() 
    dt = dt.strftime('%Y%m%d')    
    df.to_csv("momo_test.csv",index=False)
    df.to_csv(dt+"_MOMO_Info.csv",index=False)
    df.to_excel(dt+"_MOMO_Info.xlsx",index=False,engine='xlsxwriter')
    print(df.shape)
    
if __name__=="__main__":
	main()