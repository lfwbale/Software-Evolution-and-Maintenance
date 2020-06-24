#统计知识库三元组数量
file = open('../baike_triples.txt','r')
count = 0
while True:
	count = count+1
	line = file.readline()
	print(count)
	if line =='':
		break
print('The total count: '+str(count))
