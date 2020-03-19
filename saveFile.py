from dao import getContent


def saveFile(topic,content):
    '''
    将数据库取出的结果保存为文件
    :param topic: 要保存的关键词
    :param content: 要保存的内容
    :return:
    '''
    path = f'F:\毕业设计\微博数据\{topic}.txt'
    i = 0
    with open(path, 'w',encoding='utf-8') as f:
        while (i < len(content[0])):
            weibo = str(i+1) + ":\t用户:" +str(content[0][i]) + '\t内容:\t' + str(content[1][i]) + "\n"
            weibo.encode('utf-8')
            f.write(weibo)
            i += 1

if __name__ == "__main__":

    keyword = ('健康', '湖北科技学院', '5G', '中美贸易战', '垃圾分类', '教育', '医疗', '大学生', 'AI')
    keywordDb = (
    'healthy', 'hbust', 'fiveG', 'CHINA_USA', 'Classification', 'education', 'medical', 'CollegeStudents', 'AI')
    kw = 0
    while (kw < len(keyword)):
        content = getContent(keywordDb[kw])
        saveFile(keyword[kw],content)
        print(keyword[kw] + '\t保存成功！')
        kw += 1
