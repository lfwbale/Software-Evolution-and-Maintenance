import os
import pickle
import time
import requests
from bs4 import BeautifulSoup
import random
import re

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'
}

#load dictionary
def load_dic(path):
    with open(path, 'rb') as f:
        dic = pickle.load(f)
    return dic

#Metamorphic test
def find_name(dic):
	'''找出所有可能为人名的主体'''
	#要求至少要包含国籍和出生日期两种属性
	count = 0
	count2 = 0
	keys = list(dic.keys())
	for k in keys:
		nationality = ['']
		occupation = ['']
		v = dic[k]
		v_keys = list(v.keys())
		#print(v_keys)
		tag = 0
		for vk in v_keys:
			if vk == '出生日期':
				tag = 1
				#print(k,v[vk],type(v[vk]))
			if vk =='国籍' and tag == 1:
				#print(k,v[vk],type(v[vk]))
				tag = 2
				count +=1
				nationality = v[vk]

			if vk =='职业' and tag ==2:
				occupation = v[vk]

		if nationality[0] != '' and (nationality[0].count('中国')>0 or nationality[0].count('中华人民共和国')>0) :
			print(k,nationality,occupation)

	print("count = ",count)
#dictionary = load_dic('../dic/dic_test1')
#find_name(dictionary)


def gen_name_dic_file(filename,num):

	file = open(filename,'a+')
	st = time.time()
	dic = load_dic('../dic/dic_test'+str(num+1))
	ed = time.time()
	print("dic_"+str(num+1)+" has been load ! Time of loading:(s) ",ed - st)
	count = 0
	keys = list(dic.keys())
	for k in keys:
		name = k
		nationality = ['']
		birthday = ['']
		occupation = ['']
		v = dic[k]
		v_keys = list(v.keys())
		#print(v_keys)
		tag = 0
		for vk in v_keys:
			if vk == '出生日期':
				tag = 1
				birthday = v[vk]

			if vk == '国籍' and tag == 1:
				#print(k)
				nationality = v[vk]
				tag = 2

			if vk == '职业' and tag ==2 :
				occupation = v[vk]
				#print(name,occupation)
		#将所有中国人保存 稍作修改可统计外国人
		if birthday[0] != '' and (nationality[0].count('中国')>0 or nationality[0].count('中华人民共和国')>0) :
			#print(name,nationality[0],birthday[0],occupation[0])
			file.write('\n'+name+"\t"+nationality[0]+"\t"+birthday[0]+"\t"+occupation[0])
			count +=1
			continue

	print(count," name has been save...")
	file.close()
	print("done!")

#gen_name_dic_file(filename,0)
def gen_name_dic(path):
	for i in range(14):
		gen_name_dic_file(path,i)

'''
#生成全部的中国人 最终结果保存在chinese_name.txt中
dic_file = open("../dic/name_dic/chinese_name.txt",'w+')
dic_file.write("Name"+"\t"+"Nationality"+"\t"+"Birthday"+"\t"+"Occupation")
gen_name_dic("../dic/name_dic/chinese_name.txt")
'''


def baidu_name_birthday(query):
	'''查询人名的生日'''
	url = 'https://www.baidu.com/s?wd={}'.format(query)
	print("query: ",query)
	return_border = "0" #是否有框（若有框 则为摘要或精确答案）
	is_exact = "0"      #是否返回精确答案
	answer = "null"
	_from = "null"
	#记录是否成功执行查询并返回结果
	tag = '1'
	try:
		r = requests.get(url, headers = headers)
		html = r.text
		status_code = r.status_code
		#print('status_code: ', status_code)
		soup = BeautifulSoup(html, 'html.parser')
		item = soup.find('div', {'class': 'c-container'})
		tmp = item.find('div', {'class': 'c-border'})
		if tmp is not None:
			temp_exact_ans = item.find('div',{'class':'op_exactqa_s_answer'})
			if temp_exact_ans is not None:
				is_exact = "1"
				answer = temp_exact_ans.text.strip()
				#删除结果中的换行符 保证结果位于一行中
				answer.replace('\n','')
		else:
			tmp = item.find('div',{'class':'c-abstract wenda-abstract-abstract wenda-abstract-only-abstract'})
			tmp2 = item.find('div',{'class':'wenda-abstract-abstract-list c-abstract wenda-abstract-abstract wenda-abstract-only-abstract'})
			if tmp or tmp2 is not None:
				#返回了精选摘要
				return_border = "1"
			answer = 'null'
		print("answer: ", answer)
		#tmp = item.find('div', {'class': 'op_exactqa_tools'})
		tmp = item.find('div', {'class': 'c-line-clamp1'})
		#cc-line-clamp1
		if tmp is not None:
			_from = tmp.text.strip()
		else:
			_from = "null"
	except:
		tag = '0'
		print("Exception!!!")

	return return_border, is_exact, answer, _from, tag

'''
query = '山东最高的山'
boder, exact, answer, _from = baidu_name_birthday(query)
print("has border?: ",boder)
print("exact?: ",exact)
print("answer: ",answer)
print("answer from: ",_from)
'''
def delet_notes(string):
	pattern  = r'（.*）'
	pattern_2  = r'.*（'
	short_name = re.sub(pattern,'',string)
	notes =  re.sub(pattern_2,'',string)
	notes = notes.replace('）','')
	return short_name,notes


def save_name_birthday(cnt):

	file = open("../dic/name_dic/chinese_name.txt",'r')
	total_count = 0
	full_inf_count = 0
	for line in file.readlines():
		total_count += 1
		list = line.split('\t')
		if len(list)!= 4:
			print("wrong type:", str(list))
		if len(list)==4 and list[3].strip() != '':
			full_inf_count += 1

	print("total count is: ",total_count)
	print("with occupation count is: ",full_inf_count)
	#生成cnt个数的随机数 并排序 然后读取相应行的内容
	file.close()

	num_l =  random.sample(range(1,total_count),cnt+1)
	num_l.sort()
	j,k,with_occ,without_occ = 0,0,0,0

	file = open("../dic/name_dic/chinese_name.txt",'r')
	next(file)
	while k<cnt:
		line = file.readline()
		j=j+1
		if j == num_l[k]:
			k = k+1
			list = line.split('\t')
			if len(list)==4:
				list[3].strip()

			#print(list[3])
			#print("*****")

			'''
			list[0] name
			list[1] nationality
			list[2] birthday
			list[3] occupation
			'''
			print("Visit Times: ", k," line: ",num_l[k])

			if k % 10 == 0:
				interval = 5
			else:
				interval = 1 + 4 * random.random()
			time.sleep(interval)

			name = list[0]

			#处理名字后面带有解释的人物
			occupation = ''
			if name.count('（') > 0:
				name, occupation = delet_notes(name)

			source_query = name+'的生日'
			follow_up_query = "null"
			expect_answer =  list[2]
			return_border, is_exact, answer, _from, tag1= baidu_name_birthday(source_query) 

			#print(source_query)
			#print(expect_answer,return_border, is_exact, answer, _from)

			u_return_border, fu_is_exact, fu_answer, fu_from = '0','0','null','null'
		

			#follow_up query 构造
			if occupation != '' or list[3] !='':
				if list[3] != '':
					follow_up_query = list[3]+source_query
				else :
					follow_up_query = occupation + source_query
				follow_up_query = follow_up_query.replace('\n','')
			#只有拥有职业 follow_up query 才有意义
			if follow_up_query != source_query:
				fu_return_border, fu_is_exact, fu_answer, fu_from,tag2 = baidu_name_birthday(follow_up_query)
			else:
				follow_up_query = 'null'

			result_file = open("../result/name_metamorphic.txt",'a')
			result_file.write(tag1+"\t"+source_query+"\t"+expect_answer+"\t"+return_border+"\t"+is_exact+"\t"+answer+"\t"+_from+
				"\t"+follow_up_query+"\t"+u_return_border+"\t"+fu_is_exact+"\t"+fu_answer+"\t"+fu_from+"\n")
			result_file.close()

	file.close()

#save_name_birthday(300)

def swap_keywords(num,count):
	'''num为dic号 count为query数'''
	st = time.time()
	#读取dic
	dic = load_dic('../dic/dic_test'+str(num))
	ed = time.time()
	print("Time of loading: (s)", ed - st)

	#out.append('\t'.join(["query", "expect_answer", "is_exact", "answer", "_from"]))
	cnt = 0
	NUM = count
	if num==14:
		NUM = int(count/10)

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
			interval = 5
		else:
			interval = 1 + 4 * random.random()
		time.sleep(interval)

		source_query = k + "的" + vk
		follow_up_query = vk+" "+k
		expect_answer = '、'.join(vv)
		expect_answer.replace('\n','')
		#return return_border, is_exact, answer, _from, tag

		is_border,is_exact, answer, _from, is_success = baidu_name_birthday(source_query)
		fu_border,fu_exact,fu_ans,fu_from,fu_success = baidu_name_birthday(follow_up_query)

		result_file = open("../result/swap_metamorphic.txt",'a')
		result_file.write(is_success+"\t"+source_query+"\t"+expect_answer+"\t"+is_border+"\t"+is_exact+"\t"+answer+"\t"+_from+
				"\t"+follow_up_query+"\t"+fu_border+"\t"+fu_exact+"\t"+fu_ans+"\t"+fu_from+"\n")
		result_file.close()

		if answer == "":
			has_except = True
			cnt += 1

		if cnt>NUM:
			break

def swap_main():
	for i in range(11,14):
		count = 100
		swap_keywords(i+1,count)

swap_main()


	