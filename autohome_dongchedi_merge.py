import requests
import json
import pandas as pd
import numpy as np

writer = pd.ExcelWriter('./汉车型竞品车型舆情分析数据.xlsx')

# 汽车之家
car_seriesId=np.array(
    [['汉','5499'],
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
            sentimentKey=temp['SentimentKey']
            if sentimentKey==2:
                sentimentKey='不满意'
            elif sentimentKey==3:
                sentimentKey='满意'
            dic=[car,sentimentKey,opinion,volume]
            result.append(dic)
            
df=pd.DataFrame(data=result,columns=['car_type','emotion','opinion','value'],index=None)
df.drop(df[df.value==0].index,inplace=True)
df.to_excel(writer,index=False,sheet_name='汽车之家')

# 懂车帝
car_seriesId=np.array(
    [['汉EV','4300'],
    ['汉DM','4228'],
    ['海豹','5579'],
    ['极氪001','5015'],
    ['蔚来ET7','3478'],
    ['智己L7','4870'],
    ['飞凡R7','4980']]
)
# 数组存放结果
result=[]

for i in range(0,len(car_seriesId)):
    car=car_seriesId[i][0]
    id=car_seriesId[i][1]

    url=f'https://www.dongchedi.com/motor/pc/car/series/get_review_tab?aid=1839&app_name=auto_web_pc&series_id={id}&only_owner=0&car_id=0'

    headers = {
        "Accept":"*/*",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cookie":"ttwid=1%7C_RmdL2PadqyIpt9LQgmxaQbmp0ZMjSjIzRiV5LFmXOk%7C1683868713%7C8c76c28653f393a96e61be403a68e87b352be847abca27fdadcc8054603eb6cc; tt_webid=7232161008730719805; tt_web_version=new; is_dev=false; is_boe=false; Hm_lvt_3e79ab9e4da287b5752d8048743b95e6=1683868715; _gid=GA1.2.1923502872.1683868715; s_v_web_id=verify_lhk3yg5q_hIz1PIXy_aUIT_4K28_9qoJ_5KqrZz7AopsZ; city_name=%E6%83%A0%E5%B7%9E; msToken=bmxzCvYh1VJSwaCm19684Wazq8LSY4Dr1miwPlKmYhMsyAQDpWLoLdMIwQwpH5m_CRjHesk4lsWfmZSRrdAV9tScPwidjbl_gbi0hlYbh00=; _gat_gtag_UA_138671306_1=1; Hm_lpvt_3e79ab9e4da287b5752d8048743b95e6=1683871839; _ga_YB3EWSDTGF=GS1.1.1683871564.2.1.1683871839.29.0.0; _ga=GA1.2.29976944.1683868715",
        "Referer":f"https://www.dongchedi.com/auto/series/{id}",
        "Sec-Ch-Ua":"\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Platform":"\"Windows\"",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    payload={
        "aid":"1839",
        "app_name":"auto_web_pc",
        "series_id":f"{id}",
        "only_owner":"0",
        "car_id":"0"
    }

    response=requests.get(url=url,params=payload,headers=headers)
    response.encoding = 'utf-8'
    res=response.json()

    all_result = res["data"]["tab_info"]
    all_result = all_result["tag_list"]
    
    for i in range(0,len(all_result)):
        # 获取观点
        opinion=all_result[i]["tag_name"]
        # 获取观点次数
        count=all_result[i]["count"]
        # 获取观点的情感
        sentiment=all_result[i]["sentiment"]
        if sentiment==1:
            sentiment='满意'
        else:
            sentiment='不满意'
        # 数组存放将车型、情感、观点、数值 
        dic=[car,sentiment,opinion,count]
        # 在result数组中追加结果
        result.append(dic)

# 将结果写入DataFrame中
df=pd.DataFrame(data=result,columns=['car_type','emotion','opinion','value'],index=None)
df.to_excel(writer,index=False,sheet_name='懂车帝')

writer._save()
print("恭喜！........数据爬取完成！........")