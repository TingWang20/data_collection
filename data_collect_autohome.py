import requests
import json
import pandas as pd
import numpy as np

car_seriesId=np.array(
    [['汉车型','5499'],
    ['海豹','6394'],
    ['极氪001','6091'],
    ['蔚来ET7','5264'],
    ['智己L7','6012'],
    ['飞凡R7','6072']]
)
str_01='https://koubeiipv6.app.autohome.com.cn/pc/series/list?pm=3&seriesId='
str_02='&pageIndex=1&pageSize=20&yearid=0&ge=10&seriesSummaryKey=0&order=0'
result=[]
for i in range(0,len(car_seriesId)):
    car=car_seriesId[i][0]
    id=car_seriesId[i][1]

    url=str_01+id+str_02

    headers={
        'accept':'*/*',
        'accept-encoding':'gzip,deflate,br',
        'accept-language':'zh-CN,zh;q=0.9',
        'referer':f'https://k.autohome.com.cn/{id}',
        'sec-ch-ua':'".Not/A)Brand";v="99","GoogleChrome";v="103","Chromium";v="103"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/103.0.5060.53Safari/537.36',
        'x-nextjs-data':'1'
    }
    payload={
        "pm":"3",
        "seriesId":f'{id}',
        "pageIndex":"1",
        "pageSize":"20",
        "yearid":"0",
        "ge":"10",
        "seriesSummaryKey":"0",
        "order":"0"
    }

    response=requests.get(url=url,params=payload,headers=headers)
    result_json = response.json()
    result_satisfied = result_json["result"]["structuredlist"][1]
    result_1 = result_satisfied["Summary"]
    result_unsatisfied = result_json["result"]["structuredlist"][2]
    result_2 = result_unsatisfied["Summary"]
    satis_n_unsatis = [result_1,result_2]

    for i in range(0,len(satis_n_unsatis)):
        for j in range(0,len(satis_n_unsatis[i])):
            temp=satis_n_unsatis[i][j]
            opinion=temp["Combination"]
            volume=temp["Volume"]
            dic=[car,opinion,volume]
            result.append(dic)
df=pd.DataFrame(data=result,columns=['车型','观点','数值'],index=None)
df.to_excel("data.xlsx",index=False,sheet_name='汽车之家网站')