"""
    @Author:sumu
    @Date:2020-01-06 14:24
    @Email:xvzhifeng@126.com

"""

from spiders.my_spider.job51_spider import *
from utils.file_tools import *
from utils.producter_51joburl import *
from spiders.pipo_line.job51_line import *



def begin():

    condition,page_count = gain_config('./spiders.cfg')

    url_list = producter(condition,page_count+1)
    j =1
    for i in url_list:
        # 1.爬取数据
        data,e = getHtml(i)
        # 2.保存数据
        write_file_str(f'./datas/job_python/{condition+"_"+str(j)}.html','w',data)
        j+=1
        #print(data)
    # 3. 解析数据
    # 4.将解析的文件写入csv在read_data中间调用
    read_data(page_count+1)
