import re


from lxml import etree


'''
处理爬取的微博网页，提取出用户名和微博内容
'''
def clean_space(text):
    """"
    处理多余的空格
    """
    match_regex = re.compile(u'[\u4e00-\u9fa5。\.,，:：《》、\(\)（）]{1} +(?<![a-zA-Z])|\d+ +| +\d+|[a-z A-Z]+')
    should_replace_list = match_regex.findall(text)
    order_replace_list = sorted(should_replace_list,key=lambda i:len(i),reverse=True)
    for i in order_replace_list:
        if i == u' ':
            continue
        new_i = i.strip()
        text = text.replace(i,new_i)
    return text

def deal_html(data):
    '''
    处理html
    :param data: 要处理的微博html
    :return: 处理结果
    '''

    # 初始化 标准化
    html = etree.HTML(data)
    # 提取用户名和发布时间
    # users = html.xpath('//div[@class="info"]/div/a/@nick-name')
    # time = html.xpath('//div[@class="func"]/p[@class="from"]/a/text()')
    data = clean_space(data)#清除空格
    data = data.replace('\n', '').replace('\t', '').replace(' ', '')#清除空格和换行
    a_href = r'<ahref=(.*?)>(.*?)>|<imgsrc=(.*?)>(.*?)>|</a(.*?)>|</em(.*?)>|</i(.*?)>|<br/(.*?)>|<emclass(.*?)>|' \
             r'<!--card解析(.*?)>(.*?)<!--/card解析-->|<pclass="from"(.*?)>'
    data = re.sub(a_href, "", data)
    res_tr = r'<pclass="txt"node-type="feed_list_content"nick-name=(.*?)>(.*?)</p>'
    content = re.findall(res_tr, data, re.S | re.M)
    return content

def dealmweibo(data):
    data = clean_space(data)  # 清除空格
    data = data.replace('\n', '').replace('\t', '').replace(' ', '')  # 清除空格和换行
    a_href = r'</span>|<spanclass="kt"(.?)(.?)|&nbsp;|<br/>|<ahref=(.*?)]|</div>|<div>|<ahref=(.*?)>|<imgsrc=(.*?)>|' \
             r'<imgalt=(.*?)/>|<br/|<ahref=(.*?)"|https(.*?)"|组图(.*?)张|spanclass="cmt">原文转发|<spanclass="cmt"(.*?)<|<imgalt=(.*?)/,'
    res_tr = r'<spanclass="ctt">(.*?)>(.*?)</a>'
    content = re.findall(res_tr, data, re.S | re.M)
    res_tr1 =  r'<aclass="nk"(.*?)</a>'
    users = re.findall(res_tr1, data, re.S | re.M)
    a_href1 = r'href=(.*?)>'
    #d对文本再次进行处理，有待优化
    for con in range(0,len(content)):
        str1 = str(content[con])
        str1 = re.sub(a_href, "", str1)
        str1 = str1.replace("'", "")
        str1 = str1.replace(' ', '')
        str1 = str1.replace('[','')
        str1 = str1.replace(']', '')
        str1 = str1.replace('/span>',"")
        str1 = str1[2:-1]
        str2 = re.sub(a_href1, "", users[con])
        users[con] = str2
        content[con] = str1
    mycontent = [users,content]
    if len(users)!= len(content):
        return 'error'
    return mycontent

