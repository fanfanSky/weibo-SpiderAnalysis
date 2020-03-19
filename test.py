from dao import create_table
'''
建表 慎用，会清空表数据，建一张新表
'''
keywordDb = (
'healthy', 'hbust', 'fiveG', 'CHINA_USA', 'Classification', 'education', 'medical', 'CollegeStudents', 'AI')
for kw in keywordDb:
    create_table(kw)