"""
    @Author:sumu
    @Date:2020-01-06 14:35
    @Email:xvzhifeng@126.com

"""

from lxml.html import etree
import re
from utils.file_tools import *
import datetime


def read_data(page_count,filepath="./datas/job_python/"):
    """
    :param page_count: 需要爬取的页数
    :param filepath: 源文件存放的路径
    :return: 无返回值，在函数的最后将解析后的数据存储文件中
    """
    parser = etree.HTMLParser(encoding='utf-8')

    for i in range(1,page_count):
        html_tree = etree.parse(filepath+f"python_{i}.html",parser =parser)
        path = "//div[@class='dw_table']/div[@class='el']"
        jobs = html_tree.xpath(path)

        jobs_list = []

        for job in jobs:
            dict_job = std_job(job)
            jobs_list.append(dict_job)
            # job_title = job.xpath('./p/span/a')[0].text
            # job_company = job.xpath('./span/a')[0].text
            # job_place = job.xpath('./span[@class="t3"]')[0].text
            # job_salary = job.xpath('./span[@class="t4"]')[0].text
            # job_date = job.xpath('./span[@class="t5"]')[0].text

            # 加入文件到csv文件中
        #保存页面中的信息到csv文件
        save_csv(f"./handled_data/job_python_{str(datetime.datetime.now()).split(' ')[0]}.csv",jobs_list)
            #print(f"{job_title}\t {job_company} \t {job_place}\t{job_salary}\t{job_date}")

def transfermation_k(data):#提取最大最小值,单位:千每月
    """
    :param data: 处理好的工资列表
    :return: 最大薪资和最小薪资列表

    功能：把工资列表里的暑假进行进一步的分解，分成最大值和最小值的列表，其中的空值用当前数据的平均值代替
    """
    regx = re.compile(r'(\d*.?\d*)-(\d*.?\d+)')
    regx1 = re.compile(r'([\u4e00-\u9fa5])/([\u4e00-\u9fa5])')
    number = re.findall(regx, data)
    per = re.findall(regx1, data)
    if len(number) == 0 or len(per) == 0:
        return 0,0

    number = list(number[0])
    per = list(per[0])

    if '千' in per and '月' in per :
            # print('True')
        mymax = float(number[1]) * 1000
        mymin = float(number[0]) * 1000
    elif '万' in per and '月' in per :
        mymax = float(number[1]) * 10000
        mymin = float(number[0]) * 10000
    elif '万' in per and '年' in per :
        mymax = round(float(number[1]) * 10000 / 12, 2)
        mymin = round(float(number[0]) * 10000 / 12, 2)
    elif '元' in per and '天' in per :
        mymax = float(number[0])
        mymin = float(number[0])
    else :
        mymin = 0
        mymax = 0


    return mymin,mymax

def std_job(job):
    """
    功能：用于具体的解析工作，把html文件中的所有要用的信息通过lxml解析掉，从上一次的位置开始解析
    :param job: 初步解析的工作文件
    :return: 一个解析完成的字典
    """

    dic = {}
    # 取出id
    id = job.xpath('./p/input/@value')[0]
    # 取出职位名。解析式根据网页代码可得
    job_title = job.xpath('./p/span/a')[0].text
    # 对职位名进行分析，分成只有python或者id。出现python关键字的就是python，其余无法通过计算机判断的都归为it类
    ttype = [s.lower() for s in re.findall(r'[a-zA-Z]+',job_title)]
    type = 'python' if 'python' in ttype else 'it'
    # 取出公司名，和公司网站
    job_company_name = job.xpath('./span[@class="t2"]/a/@title')[0]
    job_company_link = job.xpath('./span[@class="t2"]/a/@href')[0]

    # 取出地址
    job_place = job.xpath('./span[@class="t3"]')[0].text
    # 将地址字符串以-为分隔符进行分割，
    jj_address = job_place.split('-')
    # 判断他是一个还有两个
    city = jj_address if len(jj_address)==1 else jj_address[0]
    #获取薪水
    job_salary = job.xpath('./span[@class="t4"]')[0].text
    job_salary1 =str(job_salary)
    job_date = job.xpath('./span[@class="t5"]')[0].text
    jjob_date = job_date.split('-')
    job_date_new = "2020"+job_date if jjob_date[0] == '01' else "2019"+job_date
    # 调用分解薪水的函数
    mymin,mymax = transfermation_k(job_salary1)

    # 最后我们所用到的数据类型，通过字典的方式封装进去
    dic['id'] = id
    dic['job_title'] = job_title.strip()
    dic['type'] = type
    dic['job_company_name'] =job_company_name
    dic['job_company_link'] =job_company_link
    dic['job_place'] =job_place
    dic['city'] =city
    dic['job_salary'] = job_salary
    dic['min_salary'] = mymin
    dic['max_salary'] = mymax
    dic['job_date_new'] = job_date_new
    print(dic)
    return dic


    # print(job_company_link)
    #job = {"title":job_title,"company":job_company,}
    #return {}



if __name__ == '__main__':
    read_data(2,"../../datas/job_python/")