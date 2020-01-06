## 爬虫介绍：
什么是爬虫

爬虫，即网络爬虫，大家可以理解为在网络上爬行的一直蜘蛛，互联网就比作一张大网，而爬虫便是在这张网上爬来爬去的蜘蛛咯，如果它遇到资源，那么它就会抓取下来。



## 爬虫框架

####文件目录
- datas目录:下存放原始数据
- handle_data目录:下存放经过清洗后的数据
- spider目录：存放爬虫相关的文件
    -  my_spider:爬虫源文件
    -  pipo_line:xml解析源文件
- utils：工具文件
    - file_tools:文件相关的处理方法
    - producter_51job:根据配置文件产生url
- spider:配置文件
- run.py:开始文件
- start.py :爬虫的总流程调用

### 相关知识背景

#### 用到的包或库

- requests：
    
    Requests是用Python语言编写的，基于urllib3来改写的，采用Apache2 Licensed 来源协议的HTTP库。
它比urllib更加方便，可以节约我们大量的工作，完全满足HTTP测试需求。

一句话---Python实现的简单易用的HTTP库。


    
    def getHtml(url):
        """
        :param url:  想要爬取的网址地址
        :return: 源文件和编码格式
        """
    
        # 让机器访问网址，模拟浏览器访问，具体请求头，可以在谷歌浏览器F12进入检查模式可以查看
        # 一下就是各种机型访问网站的的标志
        agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
        ]
        # 模拟一个请求头，由下面的字典组成，random.choice（）就是从agents中随机取出一个来，以达到不同人访问的目的
        # 当然除了这个方法以外还可以减慢访问的速度，因为人在访问时不可能一直点一直点，没有那么快的访问速度，所以每访问一次最好可以间隔一段时间
    
        # 还有一个问题及时由于我们访问的ip一直是一个也可能导致会被网站察觉到，所以我们可以使用代理服务器的方式。
        hs = {"User-Agent" : random.choice(agents)}
        # 利用request库发出一个get请求
        response = requests.get(url,headers =hs)
    
        # 解决乱码问题
        # 修改编码格式
        response.encoding  = response.apparent_encoding
    
        return response.text,response.encoding


- lxml：
        
      1. etree.parse()

			读取xml文件，结果为**xml对象**（不是字符串）
		2. etree.HTML(string_html)

			将字符串形势的html文件转换为xml对象
		3. etree.tostring(htmlelement, encoding="utf-8").decode("utf-8")

				etree.tostring(html,encoding="utf-8", pretty_print=True).decode()
				
	
选择器

|表达式|	描述|
|---|---|
|nodename|选取此节点的所有子节点。|
|/	|从根节点选取。|
|//	|从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。|
|.	|选取当前节点。|
|..	|选取当前节点的父节点。|
|@	|选取属性。|

- csv：一种类似于excel表的文件，用,代替了表格

        def save_csv(filepath,data,encoding='utf-8'):
            """
            :param filepath: 文件最后保存的路径
            :param data: 51job的工作信息的字典的列表
            :param encoding: 编码格式，默认utf-8，
            :return:
            """
            with open(filepath,'a+') as fp:
        
                # 获取表头列表
                headers = data and list(data[0].keys())
                print(headers)
                # 定义writer
                writer = csv.DictWriter(fp,fieldnames=headers)
                # 如果程序没有指向表头，依旧以为程序为空，没有表头，则添加表头，否则不添加表头
                if fp.tell() == 0:
                    writer.writeheader()
                # print(data)
                # for i in range(0,len(data)):
                #     print(list(data[i].values()))
                    #writer()
                # 可以直接写入字典类型的数据，但是数据的keys必须和表头的keys相等，否则会出错。
                writer.writerows(data)

- re:正则表表达式
    具体可以另一边博客[正则表达式](https://blog.csdn.net/weixin_44106306/article/details/103793636)