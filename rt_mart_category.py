'''
    Collecting the RT-Mart category tree
'''
import pandas as pd 
import numpy as np 
from bs4 import BeautifulSoup 
import requests 
from tqdm import tqdm 
import time
from datetime import date

def get_l1(url):

    # return a complete category dataframe
    url = url
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    l1_tag = ["nav01","nav02"]
    l1 = []
    l1_link = []
    for l in l1_tag:
        tag = soup.find("ul",class_="main_nav").find_all("li",class_=l)
        for t in tag:
            try:
                l1.append(t.find_all("a",href=True)[0].text)
                if t.find_all("a",href=True)[0]['href'][:4] != "http":
                    l1_link.append("https://www.rt-mart.com.tw/direct/"+t.find_all("a",href=True)[0]['href'])
                else:
                    l1_link.append(t.find_all("a",href=True)[0]['href'])
            except:
                print("exception error occur !!!")
                pass
    
    
    
    return l1,l1_link 






def get_category(category,link):
    df  = {"L1":[],"L2":[],"L3":[],"L3 link":[]}
    for ct,lk in tqdm(zip(category,link)):
        r = requests.get(lk)
        soup = BeautifulSoup(r.content,'html.parser')
        tag = soup.find("div",class_="L_Box").find_all("h3",class_="classify_title")
        tag_l3 = soup.find("div",class_="L_Box").find_all("ul")
        for t,t_l3 in zip(tag,tag_l3):
            l2 = t.find_all("a",href=True)[0].text
            l3 = t_l3.find_all("a",href=True)
            for l3_ in l3:
                df["L1"].append(ct)
                df["L2"].append(l2)
                df['L3'].append(l3_.text)
                df['L3 link'].append(l3_['href'])

    df = pd.DataFrame(df)
    df.index = np.arange(1,len(df)+1)
    return df

'''
    Crawling data from urls
    1. product
    2. price
    3. specification
    4. description
    5. category
'''
def crawler(url):

    headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    all_url ={"url":[]}
    inner_link = []
    for link in tqdm(url):
        inner_link.append(link)
        r = requests.get(link,headers=headers)
        soup = BeautifulSoup(r.content,'html.parser')
        try:
            num = soup.find("ul",class_="classify_numlist").find_all("li")
            if len(num) <= 3:
                pass
            else:
       
                if soup.find("ul",class_="classify_numlist") ==None:
                    pass
                else:
                    l = soup.find("ul",class_="classify_numlist").find_all("li",class_="list_num")
                    for i in l[1:]:
                        inner_link.append("https://www.rt-mart.com.tw/direct/"+i.find("a",href=True)['href'])
        except:
            pass
    '''
    all_url['url'] = inner_link
    all_url = pd.DataFrame(all_url)
    all_url.to_csv("url.csv",index=False)
    '''
    # getting all products links for further information extraction 
    df = {"product":[],"product link":[],"image url":[]}
    for link in tqdm(inner_link):
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.content,'html.parser')
            tag = soup.find("div",class_="classify_prolistBox").find_all("div",class_="indexProList")
            for t in tag:
                df['product'].append(t.find("h5",class_="for_proname").text)
                df['product link'].append(t.find_all('a',href=True)[0]['href'])
                i = t.find_all("img")[0]
                df['image url'].append(i['src'])

        except:
            pass
    
    


    df = pd.DataFrame(df)
    df.index = np.arange(1,len(df)+1)
    
    return df 


def page_info(df):
    headers =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHaTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    urls = df['product link']
    info = {"product number":[],"price":[],"suggested price":[],"sales":[],'description':[],"specification":[],"detailed specification":[],"category 1":[],"category 2":[],"category 3":[],"category 4":[],"category 5":[]}
    for url in tqdm(urls):
        try:
            r = requests.get(url,headers=headers)
            soup = BeautifulSoup(r.content,'html.parser')
            try:
                info['product number'].append(soup.find("div",class_="productstar_Box").find("span").text)
            except:
                info['product number'].append("None")

            try:
                s_price = soup.find("div",class_="product_PRICEBOX").find("span",class_="price_snum").text.replace("$","").replace("\r","").replace("\n","")
            
                if s_price == '' or s_price==None or s_price == " ":
                    info['price'].append(soup.find("div",class_="product_PRICEBOX").find("span",class_="price_num").text.replace("$","").replace("\r","").replace("\n",""))
                    info['suggested price'].append(soup.find("div",class_="product_PRICEBOX").find("span",class_="price_num").text.replace("$","").replace("\r","").replace("\n",""))
                
                else:
                    info['price'].append(soup.find("div",class_="product_PRICEBOX").find("span",class_="price_num").text.replace("$","").replace("\r","").replace("\n",""))
                    info['suggested price'].append(soup.find("div",class_="product_PRICEBOX").find("span",class_="price_snum").text.replace("$","").replace("\r","").replace("\n",""))
                
            except:
                info['price'].append("None")
                info['suggested price'].append("None")
            try:
                info['sales'].append(soup.find("div",class_="bonus_mbox").find('a').text)
            except:
                info['sales'].append("None")




            try:
                category = soup.find("div",class_="navigation").find_all("li")
                cg = ""
                for cate in category:
                    cg+=cate.text
                cate = cg.split(">")
                try:
                    info['category 1'].append(cate[0])
                except:
                    info['category 1'].append("None")
                try:
                    info['category 2'].append(cate[1])
                except:
                    info['category 2'].append("None")
                try:
                    info['category 3'].append(cate[2])
                except:
                    info['category 3'].append("None")
                try:
                    info['category 4'].append(cate[3])
                except:
                    info['category 4'].append("None")
                try:
                    info['category 5'].append(cate[4])
                except:
                    info['category 5'].append("None")
            except:
                info['category 1'].append("None")
                info['category 2'].append("None")
                info['category 3'].append("None")
                info['category 4'].append("None")
                info['category 5'].append("None")

        
            try:

                spec = soup.find("table",class_="title_word").text
                spec = spec.replace("\r","")
                spec = spec.replace("\n","")
                spec = spec.replace("\xa0","")
                spec = spec.replace("\t","")
                spec = spec.split(" ")
                k=0
                for i in spec:
                    if "商品規格" in i:
                        pass
                    elif "規格" in i:
                        k+=1
                        i = i.replace("規格","").replace(":","")
                        info['specification'].append(i)
                    else:
                        pass
                if k ==0:
                    info['specification'].append("None")
                '''
            if soup.find("table",class_="title_word").find("select",class_="for_input"):
                spec = soup.find("table",class_="title_word").find_all("td")[2].text
                spec = spec.replace("\r","")
                spec = spec.replace("\n","")
                spec = spec.replace("\xa0","")
                spec = spec.replace("\t","")
                spec = spec.split(" ")
                k=0
                
                for i in spec:
                    if "規格" in i:
                        k+=1
                        i = i.replace("規格","").replace(":","")
                        info['specification'].append(i)
                    else:
                        pass
                if k ==0:
                    info['specification'].append("None")
            elif "商品規格" in soup.find("table",class_="title_word").find_all("td")[0].text:
                spec = soup.find("table",class_="title_word").find_all("td")[1].text
                
                spec = spec.replace("\r","")
                spec = spec.replace("\n","")
                spec = spec.replace("\xa0","")
                spec = spec.replace("\t","")
                spec = spec.split(" ")
                k=0
                
                for i in spec:
                    if "規格" in i:
                        k+=1
                        i = i.replace("規格","").replace(":","")
                        info['specification'].append(i)
                    else:
                        pass
                if k ==0:
                    info['specification'].append("None")
            else:    
                spec = soup.find("table",class_="title_word").find_all("td")[0].text
                spec = spec.replace("\r","")
                spec = spec.replace("\n","")
                spec = spec.replace("\xa0","")
                spec = spec.replace("\t","")
                spec = spec.split(" ")
                k=0
                # debudding
                
                for i in spec:
                    if "規格" in i:
                        k+=1
                        i = i.replace("規格","").replace(":","")
                        info['specification'].append(i)
                    else:
                        pass
                if k ==0:
                    info['specification'].append("None")
                '''
            except:
                info['specification'].append("None")
        
            try:
                dspec = soup.find("div",class_="main_indexProbox01").find("div",id="product_content02").text
                dspec = dspec.replace("\r","")
                dspec = dspec.replace("\xa0","")
                dspec = dspec.replace("\t","")
                #ddes = ddes.replace("\n","")
                info['detailed specification'].append(dspec)
            except:
                info['detailed specification'].append("None")



            try:
                des = soup.find("div",class_="main_indexProbox01").find("div",id="product_content01").text
                des = des.replace("\r","")
                des = des.replace("\xa0","")
                des = des.replace("\t","")
            #des = des.replace("\n","")
                info['description'].append(des)
            except:
                info['description'].append("None")
        except:
            time.sleep(1)
            print("connection error exception")
    return info 
        


def main():
    
    dt = date.today() 
    dt = dt.strftime('%Y%m%d')    

    rt_mart_url = "https://www.rt-mart.com.tw/direct/"
    l1,l1_link = get_l1(rt_mart_url)
    df = get_category(l1,l1_link)
    df.to_excel(dt+"_RT_Mart_Category.xlsx",index=False,engine='xlsxwriter')
    df.to_csv(dt+"_RT_Mart_Category.csv",index=False)
    
    page_url = df['L3 link']
    df = crawler(page_url)
    #df.to_csv("stage01.csv",index=False)
    
    
    info = page_info(df)
    
   
    
    df['product number'] = info['product number']
    df['description'] = info['description']
    df['detailed specification'] = info['detailed specification']
    df['specification'] = info['specification']
    df['category 1'] = info['category 1']
    df['category 2'] = info['category 2']
    df['category 3'] = info['category 3']
    df['category 4'] = info['category 4']
    df['category 5'] = info['category 5']
    df['price'] = info['price']
    df['suggested price'] = info['suggested price']
    df['sales'] = info['sales']
    df = df.drop_duplicates()
    df.index = np.arange(1,len(df)+1)
    df.to_csv(dt+"_RT_Mart_info.csv",index=False)
    df.to_excel(dt+"_RT_Mart_info.xlsx",index=False,engine='xlsxwriter')

if __name__=="__main__":
    
    
    main()
   
    


    