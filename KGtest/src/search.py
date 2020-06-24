#检索特定的三元组
file = open("../baike_triples.txt",'r')
line = 0
count = 0

while line<100000:
	text = file.readline()
	line = line + 1
	#if line<10:
		#print(text)
	string = str(text).lstrip()
	if string.startswith('1669年'):
		print("NO."+str(line)+": "+string)

