
# 奥运体育主题检索

## the system description and design document

------

[TOC]

先粘一个链接

http://114.116.221.85/search.php

第一次在公网开放有后端的web，希望不要被搞，还花了一百多整了两个月服务器（实付0元）。

然后是这个仓库：

https://github.com/zhu-haifeng/IR

这个是本文html版本：

https://zhu-haifeng.github.io/IR/readme.html

### description

整个开发流程主要分为三个部分：

1. 文本采集——larbin网络爬虫完成
2. 数据处理——简单的html解析
3. 引擎建立——xunsearch构建

均在ubuntu系统上完成（虚拟机和服务器）。

##### 文本采集——larbin网络爬虫完成

这其中，1、3都是由开源的项目，但是需要一些自行配置才能使用。

文本采集部分尝试了多次，和数据处理一起，均在本地虚拟机上完成。

larbin爬虫从特定的一个	starturl，http://www.olympic.cn/开始；通过设定时间10min；爬取深度4；同域名服务器间隔时间3s；需要排除文件格式……

配置文件部分内容：

```python
...
# Larbin的名称（用于发送http头）
UserAgent Mozilla/5.0
# 第一个抽取的网址（你可以设置很多条）
startUrl http://www.olympic.cn/
...
```

运行完成，得到多个数据文件夹，每个文件夹里面最多有2000个得到的页面，和一个索引文件，索引文件中最多共有2000行，每一行是页面的url和页面文件名。

得到的部分url：

>    0 http://www.olympic.cn/
>    1 http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010102004189
>    2 http://www.sports.cn/
>    3 http://outdoor.sports.cn/
>    4 http://www.sport.gov.cn/
>    5 http://www.cbsa.org.cn/
>    6 http://www.wushu.com.cn/
>
> ...

##### 数据处理——简单的html解析

编写python脚本，遍历得到的所有页面文件，连接到对应的索引文件行的url，并通过beautifulsoup包，解析得到title和body，构建csv文件，完成预处理。

```python
from bs4 import BeautifulSoup   
import pandas as pd   
import os   
import re 
k = 0
paths = ['.//d00000//','.//d00001//','.//d00002//','.//d00003//','.//d00004//','.//d00005//','.//d00006//','.//d00007//','.//d00008//','.//d00009//','.//d00010//','.//d00011//','.//d00012//','.//d00013//','.//d00014//','.//d00015//','.//d00016//','.//d00017//','.//d00018//','.//d00019//','.//d00020//']

for i in range(len(paths)):
	path = paths[i]   
    f_index = open(path+'index','r')
    lines = f_index.readlines()
    files = os.listdir(path)
    
    # 遍历得到的所有页面文件
    for file in files:
        if file == 'index':
            continue
        id = []
        title=[]
        body = []
        urls = []
        id.append(k)
        
        # 连接到对应的索引文件行的url
        fileIndex = int(re.search('[0-9]+',file).group())
  
        url = lines[fileIndex]
        url = url[url.find('h'):].replace('\n','')
        urls.append(url)
        
		# 解析得到title和body
        with open(path+file,'rb') as f:
            soup = BeautifulSoup(f.read(),'html.parser')
            if soup.title == None or soup.title.string == None:
                title.append('')
            else:
                title.append(soup.title.string.replace('\n','').replace('\r',''))
            body.append(soup.get_text().replace('\n','').replace('\r',''))
        print(k)


        data = {'id':id,'title':title,'body':body,'urls':urls}
        print('id:\t',id,'\ttitle\t',title,'\turls\t',urls)
        
		# 解析得到title和body
        frame = pd.DataFrame(data)
        if k == 0:
            frame.to_csv('data_u.csv',encoding='utf-8',index=False)
        else :
            frame.to_csv('data_u.csv',mode = 'a+',header = False, encoding='utf-8',index=False)
    
        k = k+1

    f_index.close()
```



##### 引擎建立——xunsearch构建

xunsearch——开源免费、高性能、多功能，简单易用的专业全文检索技术方案。

参考http://www.xunsearch.com/doc/php/guide/完成索引建立、服务部署。

将上一步得到的csv文件作为数据源，编写配置文件：

```python
project.name = search

[id]
type = id

[title]
type = title

[body]
type = body

[urls]
cutlen = 100

```

可以看到共有四个字段，其中title是html页面的title，body也就是html的body。

利用工具包中Indexer.php构建索引;

开启搜索引擎后端，可以用Quest.php进行本地测试;

确认无误后，利用SearchSkel.php生成前端页面代码；

当然，生成的前端代码进行简单的修改，包括加上页面超链接、html的title、ico、页底信息等；

最后开启apache服务，将前端页面文件防导apache服务的文件夹中；

打开防火墙http端口；

虚拟机完成本地测试后，在服务器上进行相似的步骤，即可在公网访问:

http://114.116.221.85/search.php

### evaluation

先提一个比较大的影响因素。startUrl设置了国际奥委会官网，但是根本爬不了，可能是https不能爬，这是larbin使用上的一些问题。所以能得到的都是一些比较老旧的网站，样式、信息都比较滞后，并且往往缺乏维护。

通过10个查询，每个查询取前5个结果对准确性进行评估。搜索页面相似，以其中一个为例：

![](img\image-20210808172653469.png)

|查询||||||准确率|搜索耗时|
|----|--|--|--|--|--|--|--|
|冠军|0|1|1|0|1|3/5|0.0032秒|
|苏炳添|1|1|1|1|1|1| 0.0040秒 |
|杨倩|1|1|1|1|1|1|0.0155秒|
|金牌|1|1|1|1|1|1|0.0191秒|
|篮球|0|0|0|0|0|0|0.0166秒|
|体操|1|1|1|1|1|1|0.0165秒|
|教育|1|0|0|0|0|1/5| 0.0075秒 |
|东京奥运会|1|1|1|1|1|1|0.0047秒|
|北京奥运会|0|0|0|0|0|0|0.0209秒|
|北京冬奥会|1|1|1|1|0|4/5|0.0180秒|

表格中1表示相关，0表示与无关。平均准确率为0.66，搜索平均耗时0.0126秒。

### source code

由于使用到的工具包过大，在这里列出使用到的所有配置文件、关键数据、前端页面：

- [larbin配置文件](larbin-cn.conf)

- [数据预处理脚本](parser.py)

- ~~数据预处理csv(打开时应注意选择正确sd编码方式utf-8)，这个也太大了，算了，换成前2000个url~~

- [前2000个url](index)

- [前端页面](frontend/html/search.tpl)

  
