import os
import pickle
import time
import requests
from bs4 import BeautifulSoup
import random

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'
}


def load_dic(path):
    with open(path, 'rb') as f:
        dic = pickle.load(f)
    return dic

def baidu(query):
    url = 'https://www.baidu.com/s?wd={}'.format(query)
    print("query: ", query)
    is_exact, answer, _from = "0", "", ""
    try:
        r = requests.get(url, headers = headers)
        html = r.text
        status_code = r.status_code
        print('status_code: ', status_code)
        soup = BeautifulSoup(html, 'html.parser')
        item = soup.find('div', {'class': 'c-container'})
        
        tmp = item.find('div', {'class': 'op_exactqa_s_answer'})
        if tmp is not None:
            is_exact = "1"
            answer = tmp.text.strip()
        else:
            tmp = item.find('span', {'class': 'c-title-text'})
            if tmp is not None:
                print("************")
                print("here!")
                print("************")
            answer = item.h3.text.strip()
        print("answer: ", answer)
        tmp = item.find('div', {'class': 'op_exactqa_tools'})
        if tmp is not None:
            _from = tmp.text.strip()
    except:
        print("Exception!!!")

    return is_exact, answer, _from
    # for item in soup.find('div', {'id': 'content_left'}).find_all('div'):
    #     print(item)
    
    

def main():
    st = time.time()
    dic = load_dic('../dic/dic_test1')
    ed = time.time()
    print("Time of loading: (s)", ed - st)

    out = []
    out.append('\t'.join(["query", "expect_answer", "is_exact", "answer", "_from"]))

    cnt = 0
    NUM = 200
    keys = list(dic.keys())
    random.shuffle(keys)
    has_except = False

    for k in keys:
        if has_except:
            has_except = False
            continue

        v = dic[k]
        
        v_keys = list(v.keys())
        vk = random.sample(v.keys(), 1)[0]
        vv = v[vk]

        if vk == "BaiduTAG" or vk == "BaiduCARD":
            continue

        cnt += 1
        print("Visit Times: ", cnt)
        if cnt % 10 == 0:
            interval = 10
        else:
            interval = 1 + 4 * random.random()
        time.sleep(interval)

        query = k + "的" + vk
        expect_answer = '、'.join(vv)
        is_exact, answer, _from = baidu(query)

        if answer == "":
            has_except = True
        else:
            out.append('\t'.join([query, expect_answer, is_exact, answer, _from]))
        
        if len(out) > NUM:
            break

    if not os.path.exists('../result'):
        os.makedirs('../result')
    with open("../result/out.txt", 'w') as f:
        f.write('\n'.join(out))

if __name__ == "__main__":
    main()