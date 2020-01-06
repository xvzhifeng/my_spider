"""
    @Author:sumu
    @Date:2020-01-06 09:40
    @Email:xvzhifeng@126.com

"""

from lxml.html import etree

def producter(condition,page_count):
    """
    :param condition: 搜索的内容
    :param page_count: 页数
    :return: url列表
    """
    query_staring = {
        "condition" : condition,
        "page_index" : 1
    }
    url_list = []
    # 获取1到10页的数据，产生url
    for i in range(1, page_count) :
        url51job = f"https://search.51job.com/list/000000,000000,0000,00,9,99,{query_staring['condition']},2,{query_staring['page_index']}.html"
        url_list.append(url51job)

    return url_list


def gain_config(filepath) :
    """
    功能：解析配置文件，原理是和解析xml文件类同。
    :param filepath: 配置文件路径
    :return: 返回默认的配置值
    """
    config_tree = etree.parse(filepath)
    datas = config_tree.xpath('/spiders/spider[@id="job_spider"]')
    print(len(datas))

    condition = datas[0].xpath('./condition')[0].text
    page_count = datas[0].xpath('./pageAccount')[0].text

    return condition, page_count