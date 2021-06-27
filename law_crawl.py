#!/usr/bin/env python
# coding: utf-8

from lxml import html
import requests
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    df = pd.read_csv('urls.csv',index_col=0)
    df.columns=['url']
    lsi_seqs=[i.split('lsiSeq=')[-1].split("&efYd")[0] for i in df['url'].tolist()]




    url = 'https://law.go.kr/lsInfoR.do'
    result = []
    for i, lsiSeq in tqdm(enumerate(lsi_seqs)):
        try:
            form_data = {
                'lsiSeq':int(lsiSeq) # 이 부분(각법령 고유 넘버)을 가져와야함
            }
            res = requests.post(url, data=form_data)
            tree = html.fromstring(res.text)
            reg_container = tree.xpath('//div[@class="pgroup"]')
            title = tree.xpath('//div[@id="conTop"]/h2/text()')

            jo_list = [i.text_content().strip() for j in range(len(reg_container))\
                    for i in reg_container[j].xpath('.//div[@class="lawcon"]')]

            item = {
                'title':title[0],
                'contents': ' '.join(jo_list)
            }
            result.append(item)
            if len(result) >= 50:
                print('Saving data {} \t {}'.format(i-50, i))
                pd.DataFrame(result).to_csv('./data/law_{}_{}.csv'.format(i-49,i), index=False)
                result=[]
        except Exception:
            continue






