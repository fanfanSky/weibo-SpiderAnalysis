from snownlp import SnowNLP
import matplotlib.pyplot as plt

def transval(s):
	dat=SnowNLP(s).sentiments#情感分析
	return (round(dat*100,2),round((1-dat)*100,2) )  # 将数值转为百分数


def sfilter(in_str):#返回过滤后语句
	out_str=''
	for i in range(len(in_str)):
		if is_uchar(in_str[i]):
			out_str=out_str+in_str[i]
		else:
			out_str=out_str+' '
	return out_str

def is_uchar(uchar):
	"""判断一个unicode是否是汉字"""
	if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
			return True
	"""判断一个unicode是否是数字"""
	if uchar >= u'\u0030' and uchar<=u'\u0039':
			return False
	"""判断一个unicode是否是英文字母"""
	if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
			return False
	if uchar in ('-',',','，','。','.','>','?'):
			return False
	return False


		   
def autolabel(rects,type):
	for rect in rects:
		height = rect.get_height()
		if type==1:
			plt.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%d'%height,
				ha='center', va='bottom')
		else:
			plt.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%2.1f'%height,
				ha='center', va='bottom')   

def showdata(file):
	data=[]
	y=[]
	with open('./result/{}-res.txt'.format(file),'r',encoding='utf-8') as f:
		for line in f:
			s=float(line.strip().split('%')[0].split('比')[-1])/100
			data.append(s)
	plt.figure()     
	plt.rc('font', family='SimHei', size=13)
	plt.hist(data, bins=20, range=(0,1),density=False,align='mid', color='deepskyblue')#画分布图
	# rect=plt.bar(x,y, width, color='blue',label=legend)
	plt.xlabel('rate')
	plt.ylabel('number')
	# plt.xticks(x+width/2, label, rotation=75)
	plt.xlim(0,1)
	plt.title('微博评论情感分布')
	plt.show()