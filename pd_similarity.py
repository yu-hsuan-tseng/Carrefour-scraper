import jieba
import numpy as np
import pandas as pd
import re
from tqdm import tqdm



class Comparing:

    def __init__(self):
        # self.data1 is the spec from carrefour
        # self.data2 is the spec extracted by our tool
        self.data1 = pd.read_csv("xx.csv")
        self.data2 = pd.read_csv("xx.csv")
        
    def word2vec(self,s1,s2):

        cut1 = jieba.cut(s1)
        cut2 = jieba.cut(s2)
        list1 = (",".join(cut1)).split(",")
        list2 = (",".join(cut2)).split(",")
        keyword = list(set(list1+list2))
        vector1 = np.zeros(len(keyword))
        vector2 = np.zeros(len(keyword))
        for i in range(len(keyword)):
            for j in range(len(list1)):
                if keyword[i] == list1[j]:
                    vector1[i]+=1
            for k in range(len(list2)):
                if keyword[i] == list2[k]:
                    vector2[i]+=1
        return vector1,vector2


    def comparing(self):

        df = {"carrefour productNumber":[],"carrefour product":[],"RT Mart productNumber":[],"RT Mart product":[]}
        data1 = self.data1
        data2 = self.data2
        print(data1.shape)
        print(data2.shape)
        data1 = data1[:1000]
        data2 = data2[:3000]
        word2vec = self.word2vec
        for s1,idx1 in tqdm(zip(data1['product'],data1['單品長代號'])):
            for s2,idx2 in zip(data2['product'],data2['product number']):
                try:
                    vector1,vector2 = word2vec(s1,s2)
                    similarity=float(np.dot(vector1,vector2)/(np.linalg.norm(vector1)*np.linalg.norm(vector2)))
                    if similarity > 0.8:
                        df['carrefour productNumber'].append(idx1)
                        df['carrefour product'].append(s1)
                        df['RT Mart productNumber'].append(idx2)
                        df['RT Mart product'].append(s2)

                except:
                    pass
        df = pd.DataFrame(df)
        return df
        
if __name__=="__main__":

    comp =Comparing()
    df = comp.comparing()
    df.to_csv("compare_result.csv",index=False)
