#-*-coding:utf-8-*-
import requests
import re
from urllib.parse import urlunsplit
from urllib.request import ProxyHandler,build_opener
import json

import os
from urllib.request import urlopen

from urllib.parse import urlparse
import time

with open("院校地区.txt","r",encoding="utf-8") as f:
    region_id_s=f.read()
    region_id_s=region_id_s.replace("，",",")
    region_id_d=json.loads(region_id_s)

def gethtml(url):
    headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
    }#firefox浏览器表头
    req=requests.get(url,headers=headers,timeout=10)
    print("加载成功:",url)
    return req.text

#https://yz.chsi.com.cn/sch/search.do?ssdm=11&yxls=&zhx=1

def make_sch_url(region_id):
    netloc='yz.chsi.com.cn'
    scheme='https'
    path='/sch/search.do'
    params=''
    #region_id
    query='ssdm=%s&yxls=&zhx=1' %(str(region_id))
    fragment=''
    url=urlunsplit([scheme,netloc+path,params,query,fragment])
    return url

def ana_sch_name(html):
    html=re.sub('<b>|</b>|<span.*?>|</span>| |\\r|\\n|&nbsp|;','',html)#去掉这些东西，方便查找
    pattern_1=re.compile(
        '<divclass="yxk-table"><tableclass="ch-table">(.*?)</table>'
        )#正则表达式
    #re.S#换行相关
    items_1=re.findall(pattern_1,html)[0]
    pattern_2=re.compile(
        '<tr><td><a.*?>(.*?)</a>'
        )#正则表达式
    #re.S#换行相关
    items_2=re.findall(pattern_2,items_1)
    return items_2

l_out=[]
for region_id in list(region_id_d.values()):
    url=make_sch_url(region_id)
    html=gethtml(url)#得到网页源码
    l=ana_sch_name(html)
    #[(region_id,i) for i in l]
    l_out+=[(region_id,i) for i in l]

#https://yz.chsi.com.cn/zsml/querySchAction.do?ssdm=11&dwmc=北京大学&mldm=&mlmc=&yjxkdm=0854&xxfs=&zymc=

def make_zsml_url(region_id,name):
    netloc='yz.chsi.com.cn'
    scheme='https'
    path='/zsml/querySchAction.do'
    params=''
    #region_id
    query='ssdm=%s&dwmc=%s&mldm=zyxw&mlmc=&yjxkdm=0854&xxfs=&zymc=' %(str(region_id),str(name))
    fragment=''
    url=urlunsplit([scheme,netloc+path,params,query,fragment])
    return url

#'ssdm=12&dwmc=天津大学&mldm=zyxw&mlmc=&yjxkdm=0854&zymc=&xxfs=&pageno=2'
def make_zsml_url_pg2(region_id,name):
    netloc='yz.chsi.com.cn'
    scheme='https'
    path='/zsml/querySchAction.do'
    params=''
    #region_id
    query='ssdm=%s&dwmc=%s&mldm=&mlmc=&yjxkdm=0854&xxfs=&zymc=&pageno=2' %(str(region_id),str(name))
    fragment=''
    url=urlunsplit([scheme,netloc+path,params,query,fragment])
    return url

def make_zsml_url_pg3(region_id,name):
    netloc='yz.chsi.com.cn'
    scheme='https'
    path='/zsml/querySchAction.do'
    params=''
    #region_id
    query='ssdm=%s&dwmc=%s&mldm=&mlmc=&yjxkdm=0854&xxfs=&zymc=&pageno=3' %(str(region_id),str(name))
    fragment=''
    url=urlunsplit([scheme,netloc+path,params,query,fragment])
    return url

def make_zsml_url_pg4(region_id,name):
    netloc='yz.chsi.com.cn'
    scheme='https'
    path='/zsml/querySchAction.do'
    params=''
    #region_id
    query='ssdm=%s&dwmc=%s&mldm=&mlmc=&yjxkdm=0854&xxfs=&zymc=&pageno=4' %(str(region_id),str(name))
    fragment=''
    url=urlunsplit([scheme,netloc+path,params,query,fragment])
    return url

def ana_zsml_name(html):
    html=re.sub('<b>|</b>|<span.*?>|</span>| |\\r|\\n|&nbsp|;','',html)#去掉这些东西，方便查找
    pattern_1=re.compile(
        '<tableclass="ch-table">.*?<tbody>(.*?)</tbody>'
        )#正则表达式
    #re.S#换行相关
    items_1=re.findall(pattern_1,html)[0]
    pattern_2=re.compile(
        '<tr>(.*?)</tr>'
        )#正则表达式
    #re.S#换行相关
    items_2=re.findall(pattern_2,items_1)
    l1=[]
    for data_tr in items_2:
        pattern_3=re.compile(
            '<td.*?>(.*?)</'
            )#正则表达式
        #re.S#换行相关
        items_3=re.findall(pattern_3,data_tr)
        l=[]
        if items_3!=[]:
            pattern_4=re.compile(
                '<ahref="(.*?)"'
                )#正则表达式
            #re.S#换行相关
            items_3[7]=re.findall(pattern_4,items_3[7])[0]
            pattern_5=re.compile(
                "<script.*?cutString(.*?)\)\)"
                )#正则表达式
            #re.S#换行相关
            items_3[6]=re.findall(pattern_5,items_3[6])[0]
            l=[items_3[0],items_3[1],items_3[2],items_3[3],items_3[4],items_3[6],items_3[7]]
            #"考试方式,    院系所,    专业	   ,研究方向	,学习方式,	拟招生人数	,考试范围
        l1.append(l)
    return l1

l_out2=[]

# url=make_zsml_url(l_out[0][0],l_out[0][1])
# html=gethtml(url)
# l=ana_zsml_name(html)
# l_out2+=[(l_out[0][1],l)]




for aggr in l_out:
    region_id=aggr[0]
    name=aggr[1]
    url=make_zsml_url(region_id,name)
    html=gethtml(url)
    l=ana_zsml_name(html)
    if len(l)>=30:
        #华中科技大学除外
        if name=="华中科技大学":
            pass
        else:
            url=make_zsml_url_pg2(region_id,name)
            html=gethtml(url)
            l+=ana_zsml_name(html)
    if len(l)>=60:
        url=make_zsml_url_pg3(region_id,name)
        html=gethtml(url)
        l+=ana_zsml_name(html)
    if len(l)>=90:
        url=make_zsml_url_pg4(region_id,name)
        html=gethtml(url)
        l+=ana_zsml_name(html)
    l_out2+=[(name,l)]


def find_max(l_out2):
    max_name=''
    max_num=0
    for i in l_out2:
        if (len(i[1])>max_num):
            max_num=len(i[1])
            max_name=i[0]
    return max_name,max_num


#多于30个要翻页

def find_more_30(l_out2):
    for i in l_out2:
        if (len(i[1])>=30):
            print(i[0],len(i[1]))

#怎么处理翻页问题

def make_yuan_url(url_part):
    netloc='yz.chsi.com.cn'
    scheme='https'
    path=url_part
    params=''
    #region_id
    query=''
    fragment=''
    url=urlunsplit([scheme,netloc+path,params,query,fragment])
    return url

def deal_one_url(yuan_url):
    html=gethtml(yuan_url)
    html=re.sub('<b>|</b>| |\\r|\\n|&nbsp|;','',html)#去掉这些东西，方便查找
    pattern_1=re.compile(
        '<tbodyclass="zsml-res-items"><tr>(.*?)</tr>'
        )#正则表达式
    #re.S#换行相关
    #items_1=re.findall(pattern_1,html)[0]
    items_1=re.findall(pattern_1,html)
    l_tem=[]
    for huo in items_1:
        pattern_2=re.compile(
            '<td>(.*?)<span'
            )#正则表达式
        #re.S#换行相关
        items_2=re.findall(pattern_2,huo)
        l_tem.append(items_2)
    return l_tem

for i in range(len(l_out2)):
    name=l_out2[i][0]
    data=l_out2[i][1]
    add=0
    for j in range(len(data)):
        part_url=data[j+add][6]
        l=deal_one_url(make_yuan_url(part_url))
        if len(l)>1:
            data[j+add]+=l[0]
            for k in range(1,len(l)):
                data.insert(j+add+1,['']*7+l[k])
                add+=1
        else:
            data[j+add]+=l[0]

#l.insert(6,7)

#输出为csv
import os
os.getcwd() #获取当前工作路径

from pandas import Series,DataFrame
#data = {"name":['google','baidu','yahoo'],"marks":[100,200,300],"price":[1,2,3]}

#f1 = DataFrame(data)

# df = DataFrame(columns=('lib', 'qty1', 'qty2'))#生成空的pandas表
# for i in range(5):#插入一行
#     df.loc[i] = [randint(-1,1) for n in range(3)]

df=DataFrame(columns=('学校名','考试方式','院系所','专业','研究方向','学习方式','拟招生人数','政治','外语','业务课一','业务课二'))
#8列
count=0
for i in l_out2:
    #学校单行
    df.loc[count] = [i[0]]+['']*10
    count+=1
    for data in i[1]:
        df.loc[count] =['']+[data[data_id] for data_id in range(len(data)) if data_id != 6]
        count+=1


df=df[~df['考试方式'].isin(['单考'])]
df=df[~df['学习方式'].isin(['非全日制'])]


df.to_csv('0854最多翻4页.csv')
print(find_more_30(l_out2))