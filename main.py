import jieba
from  util import sfilter,transval,showdata

def stopwordslist():  # 获取停用词词典stopwords
	stopwords=[]
	with open("./stopwords.txt", "r", encoding='utf-8') as file:
		for line in file:
			stopwords.append(line.strip())
	return stopwords

def saveresults(fname,linenum,pos,neg):#保存分析结果
	with open('./result/{}-res.txt'.format(fname), "a+", encoding='utf-8') as f:
		f.write(linenum+': 消极百分比{}% 积极百分比{}%'.format(pos,neg) + '\n')

def readfile(filename):#去除停用词
	stopwords = stopwordslist()
	with open(filename, "r", encoding='utf-8') as f:
		for line in f:
			s=sfilter(line.strip().split('内容:')[-1])#过滤特殊字符
			linenum = line.strip().split(':')[0]#获取行号
			sentencecut =jieba.cut(line.strip())#结巴分词处理
			newsentence=''
			for word in sentencecut:
				if word not in stopwords:
					if word !='\t'  and '\n':
							newsentence+=word
			pos,neg=transval(newsentence) #获取情感分析结果
			saveresults(filename.split('/')[-1].split('.')[0],linenum,pos,neg)
			print(linenum,pos)


if __name__ == '__main__':#主程序入口
	# readfile('./data/5G.txt')
	# readfile('./data/AI.txt')
	# readfile('./data/大学生.txt')
	# readfile('./data/湖北科技学院.txt')
	# readfile('./data/中美贸易战.txt')
	# readfile('./data/教育.txt')
    readfile('./data/垃圾分类.txt')
    
	# showdata('大学生')
	# showdata('湖北科技学院')
	# showdata('5G')
	# showdata('中美贸易战')
	# showdata('教育')
    showdata('垃圾分类')


