import re
def read_database(filename):
	'''读取知识库'''
	file = open(filename,'r')
	line = 0
	while line<10000:
		text = file.readline()
		line = line + 1
		print("NO."+str(line)+": "+text)

#读取知识库
#read_database("../baike_triples.txt")

def static_result(filename):
	'''统计结果'''
	file = open(filename,'r')
	next(file)
	count = 0
	exact_count = 0
	from_baike = 0
	for line in file:
		#print(str(count)+":"+line)
		list = line.split('\t')
		if len(list)>2:
			count = count+1
			if list[2] == '1':
			#统计搜索答案与预期答案一致的query
				exact_count = exact_count+1
				#print(list)
				file_result = open('../exact_result.txt','a')
				string = list[0]+'\t'+list[1]+'\t'+list[2]+'\t'+list[3]+'\t'+list[4]
				#string = list[0]+'\t'+list[1]
				file_result.write(string+'\n') 
				if list[-1] == "来自百度百科\n":
				#统计没有返回答案框的query
					from_baike = from_baike+1
				else :
					print(list)

		
	print("the total query number:"+str(count))
	print("the exact_ans count:"+str(exact_count))
	print("the ans form baike:"+str(from_baike))

	static_list=[count,exact_count,from_baike]
	print(static_list)
	return static_list

#统计单个文件的结果
def single_ans(filename):
	l = static_result(filename)
	print(l[0],l[1],l[2])
#single_ans("../result/result_5m/2nd/out9.txt")

#寻找不符合条件的query
def spe(filename):
	file = open(filename,'r')
	next(file)
	for line in file:
		list = line.split('\t')
		if len(list)>2:
			if len(list) != 5:
				print("问题2:"+str(list))
		else:
			print("问题1："+str(list))

#spe("../result/result_5m/2nd/out10.txt")

'''
file_result = open('../exact_result.txt','w')
file_result.write('query'+'\t'+'expect_answer'+'\t'+'is_exact'+'\t'+'answer'+'\t'+'answer_from'+'\n')
file_result.close()
query_count = 0
right_ans = 0
from_baike = 0
for i in range(1,11):
	print("text"+str(i)+":")
	list = static_result("../result/result_5m/1st/out"+str(i)+".txt")
	query_count += list[0]
	right_ans += list[1]
	from_baike += list[2]
	print("")
print(query_count)
print(right_ans)
print(from_baike)
'''
#name occupation 实验数据统计
def normalize_birth(string1,string2):
	pattern = '[^1-9]'
	result1 = re.sub(pattern,'',string1)
	result2 = re.sub(pattern,'',string2)
	if result1==result2:
		return 0
	else:
		if result1.find(result2)!=-1:
			return 1
		else:
			return 2

def static_name_metamorphic(filename):
	'''
	['1',
	'马智君的生日', '1957年', '0', '1', '1957年',
	'null', '教育 教师马智君的生日', '0', '0', 'null', 'null']
	'''
	successful_cnt = 0              #成功测试次数
	is_exact_cnt = 0                #返回精确结果个数
	right_ans_cnt = 0               #正确结果个数
	wrong_ans_cnt = 0               #不正确结果个数
	metamorphic_cnt = 0             #执行follow up query 次数
	fu_query_abstract_cnt = 0        #follow up query 返回摘要
	fu_query_isexact_cnt = 0         #follow_up query返回精确结果
	matrix = [[0,0],[0,0]]
	'''
	返回精确结果有followup 返回精确结果无followup
	不返回精确结果有followup 不返回无followup
	'''
	file = open(filename,'r')
	lines = file.readlines()
	for line in lines:
		try:
			list = line.strip().split('\t')
			if list[0] == '1' :
				successful_cnt += 1
			if list[3] == '1':
				print("soure query abstract ans：",list)
			if list[4] == '1':
				is_exact_cnt += 1
				compare = normalize_birth(list[2],list[5])
				if compare ==0:
					right_ans_cnt += 1
				elif compare ==1:
					print("格式或答案不准：",list)
				else:
					#print("different person：",list)
					wrong_ans_cnt += 1

				if list[7]!='null':
					matrix[0][0] += 1
				else:
					matrix[0][1] += 1
			if list[7] != 'null':
				metamorphic_cnt += 1
				if list[4] == '0':
					matrix[1][0] +=1
			if list[7]=='null' and list[4]=='0':
				matrix[1][1] += 1
			if list[8]!='0' or list[9]!='0':
				print("follow_up query get ans: ",list)
				if list[8] != '0':
					fu_query_abstract_cnt += 1
				if list[9] != '0':
					fu_query_isexact_cnt += 1
			#print(list)
		except:
			print(line)
	file.close()
	print("成功执行次数： ",successful_cnt)
	print("精确结果个数： ",is_exact_cnt)
	print("其中正确结果： ",right_ans_cnt,"错误结果： ",wrong_ans_cnt)
	print("存在follow_up 个数:",metamorphic_cnt)
	print(matrix)


#static_name_metamorphic("name_metamorphic.txt")
#print(normalize_birth('1973年11月7日','1973年11月7日'))

def swap_static(filename):
	'''统计交换主体-属性后的query信息'''
	total_cnt = 0
	successful_cnt = 0
	source_query_ans = 0
	source_query_border = 0
	fu_query_ans = 0
	fu_query_border = 0
	file = open(filename,'r')
	for line in file.readlines():
		total_cnt += 1
		try:
			list = line.strip().split('\t')

			#解决答案中存在换行符的问题
			if len(list)<12:
				print(list)
			if list[0] == '1':
				successful_cnt += 1
			if list[4] == '1':
				source_query_ans += 1
			if list[3] == '1':
				source_query_border += 1
				print("source_query_border:",list)
			if list[9] == '1':
				fu_query_ans += 1
				print("follow_up query ans",list)
			if list[8] == '1':
				fu_query_border += 1
				print("follow_up query extract",list)

		except:
			print(line)
	print("total query:",total_cnt)
	print("successful query:",successful_cnt)
	print("source query return exact ans:",source_query_ans,"  return extract:",source_query_border)
	print("follow up query return exact ans:",fu_query_ans," return extract:",fu_query_border)

swap_static('../result/swap_metamorphic.txt')
