
'''
    Collecting the A-Mart category tree
    date : 2021/01/24
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

    dt = date.today() 
    dt = dt.strftime('%Y%m%d')  
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
        '''
        opener = req.build_opener()
        opener.addheaders = [{'User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}]
        req.install_opener(opener)
        response =  req.urlopen(link)
        r = response.read().decode('utf-8')
        '''
        browser.get(link)
        soup = BeautifulSoup(browser.page_source,'html.parser')
        c1 = soup.find("div",class_="head").find('a',href=True).text
        c2 = soup.find("div",class_="second").find('a',href=True).text
        all_c3 = soup.find("ul",class_="next_nave_box amart_nav").find_all("div",class_="third")
        for c3 in all_c3:
            
            try:
                c3_ = c3.find('a',href=True).text 
                df['L1'].append(c1)
                df['L2'].append(c2)
                df['L3'].append(c3_)
                if "https" in c3.find('a',href=True)['href']:
                    df['L3 link'].append(c3.find('a',href=True)['href'])
                else:
                    df['L3 link'].append("https://shopping.friday.tw"+c3.find('a',href=True)['href'])
                
                        
                        
            except:
                df['L1'].append(c1)
                df['L2'].append(c2)
                df['L3'].append(c3_)
                df['L3 link'].append("")
    link_info = {'links':[]}
    for link in tqdm(df['L3 link']):
        
        if link=="None":
            pass
        else:
            try:    
                '''
                opener = req.build_opener()
                opener.addheaders = [{'User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}]
                req.install_opener(opener)
                response =  req.urlopen(link)
                r = response.read().decode('utf-8')
                '''
                browser.get(link)
                soup = BeautifulSoup(browser.page_source,'html.parser')
                p_links = soup.find('ul',class_="fourth_nave_box")
                inner = p_links.find_all("li")
                for j in inner:
                    product_links.append("https://shopping.friday.tw"+j.find('a',href=True)['href'])
                    link_info['links'].append("https://shopping.friday.tw"+j.find('a',href=True)['href'])
            except:
                time.sleep(5)
                pass
            
    df = pd.DataFrame(df)
    df.index = np.arange(1,len(df)+1) 
    df.to_csv(dt+"_A_Mart_Category.csv",index=False)
    df.to_excel(dt+"_A_Mart_Category.xlsx",index=False,engine='xlsxwriter')
    browser.quit()
    link_info = pd.DataFrame(link_info)
    link_info.to_csv(dt+"_amart_link.csv",index=False)
    
    return df,product_links




def page_info(urls):

    '''
        Has potential issue with the multiple pages 
    '''
    dt = date.today() 
    dt = dt.strftime('%Y%m%d')  
    browser = webdriver.Chrome(executable_path="./chromedriver")
    df = {"product":[],"product link":[],'image url':[],"product number":[],"price":[],"suggested price":[],"sales":[],'description':[],"specification":[],"detailed specification":[],"category 1":[],"category 2":[],"category 3":[],"category 4":[],"category 5":[]} 
    
    for url in tqdm(urls):
        try:
            
            browser.get(url)
            time.sleep(0.5)
            soup = BeautifulSoup(browser.page_source,'html.parser')
            #tag = soup.find("ul",id_="prodlist").find_all("li")

            if soup.find("div",class_="prodlist_box").find("ul",class_="content"):
                tag = soup.find("div",class_="prodlist_box").find("ul",class_="content")
        
                for t in tag:
                
                    df['product link'].append(url)
                    df['product number'].append("")
                    try:
                        df['suggested price'].append(t.find("p",class_="prod_price").text)
                    except:
                        df['suggested price'].append("")
                    df['sales'].append("")
                    df['description'].append("")
                    df['specification'].append("")
                    df['detailed specification'].append("")
                    df['category 1'].append("")
                    df['category 2'].append("")
                    df['category 3'].append("")
                    df['category 4'].append("")
                    df['category 5'].append("")

                    try:
                        df['product'].append(t.find('p',class_="product_name").text)
                    except:
                        df['product'].append("")
                    try:
                        df['price'].append(t.find("p",class_="prod_price").text)
                    except:
                        df['price'].append("")
                    try:
                        df['image url'].append(t.find("div",class_="prod_photo").find('img')['src'])
                    except:
                        df['image url'].append("")

            elif soup.find("div",class_="prodlist_box").find("ul",class_="content array"):
                tag = soup.find("div",class_="prodlist_box").find("ul",class_="content array")
                prod = tag.find_all("li")
                in_link = []
                for l in prod:    
                    in_link.append("https://shopping.friday.tw"+l.find('a',href=True)['href'])
                for l in in_link:
                    browser.get(l)
                    soup = BeautifulSoup(browser.page_source,'html.parser')
                    
                    try:
                        df['product'].append(soup.find('h1',class_="product_name").text)
                    except:
                        df['product'].append("")

                    try:
                        df['product link'].append(l)
                    except:
                        df['product link'].append("")
                    
                    try:
                        df['image url'].append("https"+soup.find("div",class_="prodimg").find('img')['src'])
                    except:
                        df['image url'].append("")


                    try:
                        df['price'].append(soup.find("div",class_="attract_block").find("span",class_="price_txt").text)
                    except:
                        df['price'].append("")

                    try:
                        df['detailed specification'].append(soup.find("div",class_="content specification_box").text)
                    except:
                        df['detailed specification'].append("")

                    try:
                        df['product number'].append(soup.find("div",class_="product_id").find("span",class_="e3_pid").text)
                    except:
                        df['product number'].append("")

                    try:
                        df['suggested price'].append(soup.find("span",class_="pricing").text)
                    except:
                        df['suggested price'].append("")
                    
                    try:
                        df['description'].append(soup.find("h3",class_="introduction").text)
                    except:
                        df['description'].append("")
                    
                    
                    try:
                        cat = soup.find("div",class_="path").find_all("a",href=True)
                        df['category 1'].append(cat[1].text)
                    except:
                        df['category 1'].append("")

                    try:
                        df['category 2'].append(cat[2].text)
                    except:
                        df['category 2'].append("")

                    try:
                        df['category 3'].append(cat[3].text)
                    except:
                        df['category 3'].append("")

                    try:
                        df['category 4'].append(cat[4].text)
                    except:
                        df['category 4'].append("")

                    try:
                        df['category 5'].append(cat[5].text)
                    except:
                        df['category 5'].append("")

                    df['specification'].append("")
                    df['sales'].append("")
                    
            else:   
                pass
            
        except:
            print('exception occurs in :'+ url)
            time.sleep(1.5)
            pass
    
    browser.quit()
    print(len(df['product']))
    print(len(df['product link']))
    print(len(df['product number']))
    print(len(df['image url']))
    print(len(df['price']))
    print(len(df['suggested price']))
    print(len(df['specification']))
    print(len(df['detailed specification']))
    print(len(df['description']))
    print(len(df['category 1']))
    print(len(df['category 2']))
    print(len(df['category 3']))
    print(len(df['category 4']))
    print(len(df['category 5']))
    print(len(df['sales']))
    #print(df)

    df = pd.DataFrame(df)
    df = df.drop_duplicates()
    df.index = np.arange(1,len(df)+1)
    df.to_csv(dt+"_A_Mart_info.csv",index=False)
    df.to_excel(dt+"_A_Mart_info.xlsx",index=False,engine='xlsxwriter')
    return df


def main():

    
    url = "https://shopping.friday.tw/1/699.html"
    soup = get_page(url)
    df,links = get_category2(soup)
    #df = pd.read_csv("20210302_amart_link.csv")
    df = page_info(links)
    print(df.shape)
    
 
if __name__=="__main__":
    
    main()

