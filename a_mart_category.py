'''
    Collecting the A-Mart category tree
'''
import pandas as pd 
import numpy as np 
from bs4 import BeautifulSoup 
import requests 
from selenium import webdriver
from tqdm import tqdm 
from time import sleep
from datetime import date
import time
import ssl
import urllib.request as req

ssl._create_default_https_context = ssl._create_unverified_context

def get_page(url):
    browser = webdriver.Chrome(executable_path='./chromedriver')
    browser.get(url)
    soup = BeautifulSoup(browser.page_source,'html.parser')
    time.sleep(1)
    browser.quit()
    return soup


'''
    solution-2
'''
def get_category2(soup):
    #headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    tag = soup.find("div",class_="menu")
    l1 = ["menu1","menu1 no-br","menu2","menu3","menu2 no-br","menu3 no-br","menu4 no-br","menu4"]
    df = {'L1':[],"L2":[],'L3':[],'L3 link':[]}
    links = []
    product_links = []
    browser = webdriver.Chrome(executable_path='./chromedriver')
    for l in tqdm(l1):
        time.sleep(1)
        all_l1 = tag.find_all("li",class_=l)
        for l1_link in all_l1:
            link = l1_link.find_all('a',href=True)[0]['href']
            links.append(link)
    links = set(links)

    for link in tqdm(links):
      
        opener = req.build_opener()
        opener.addheaders = [{'User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}]
        req.install_opener(opener)
        response =  req.urlopen(link)
        r = response.read().decode('utf-8')
        
        soup = BeautifulSoup(r,'html.parser')
        c1 = soup.find("div",class_="head").find('a',href=True).text
        c2 = soup.find("div",class_="second").find('a',href=True).text
        all_c3 = soup.find("ul",class_="next_nave_box amart_nav").find_all("div",class_="third")
        for c3 in all_c3:
            
            try:
                c3_ = c3.find('a',href=True).text 
                df['L1'].append(c1)
                df['L2'].append(c2)
                df['L3'].append(c3_)
                df['L3 link'].append("https://shopping.friday.tw"+c3.find('a',href=True)['href'])
                
                        
                        
            except:
                df['L1'].append(c1)
                df['L2'].append(c2)
                df['L3'].append(c3_)
                df['L3 link'].append("None")

    for link in tqdm(df['L3 link']):
        
        if link=="None":
            pass
        else:
            
            
            try:
                
                opener = req.build_opener()
                opener.addheaders = [{'User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}]
                req.install_opener(opener)
                response =  req.urlopen(link)
                r = response.read().decode('utf-8')
                soup = BeautifulSoup(r,'html.parser')
                p_links = soup.find('ul',class_="fourth_nave_box")
                inner = p_links.find_all("li")
                for j in inner:
                    product_links.append("https://shopping.friday.tw"+j.find('a',href=True)['href'])
            except:
                time.sleep(5)
                pass
            
    df = pd.DataFrame(df)
    df.index = np.arange(1,len(df)+1) 
    browser.quit()
    return df,product_links




def page_info(urls):

    '''
        Has potential issue with the multiple pages 
    '''
    browser = webdriver.Chrome(executable_path="./chromedriver")
    df = {"product":[],"price":[],'image url':[]} 
    for url in tqdm(urls):
        
        
        try:
            browser.get(url)
            time.sleep(0.5)
            soup = BeautifulSoup(browser.page_source,'html.parser')
            #tag = soup.find("ul",id_="prodlist").find_all("li")
            tag = soup.find("div",class_="prodlist_box").find("ul",class_="content")
        
            for t in tag:
            
                try:
                    df['product'].append(t.find('p',class_="product_name").text)
                except:
                    df['product'].append("None")
                try:
                    df['price'].append(t.find("p",class_="prod_price").text)
                except:
                    df['price'].append("None")
                try:
                    df['image url'].append(t.find("div",class_="prod_photo").find('img')['src'])
                except:
                    df['image url'].append("None")
              
            
            
            
        except:
            print('exception occurs')
            
            pass
    browser.quit()
    df = pd.DataFrame(df)
    df.index = np.arange(1,len(df)+1)
    return df




if __name__=="__main__":
    
    dt = date.today() 
    dt = dt.strftime('%Y%m%d')    
  
    url = "https://shopping.friday.tw/1/699.html"
    soup = get_page(url)
    df,links = get_category2(soup)
    df = page_info(links)
   
    df.to_csv(dt+"_A_Mart_info.csv",index=False)
    print(df.shape)