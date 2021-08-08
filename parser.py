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

    for file in files:
        if file == 'index':
            continue
        id = []
        title=[]
        body = []
        urls = []
        id.append(k)
        fileIndex = int(re.search('[0-9]+',file).group())
        
        #url = lines[k%2000]
        #url = url[url.find('h'):].replace('\n','')
        url = lines[fileIndex]
        url = url[url.find('h'):].replace('\n','')
        urls.append(url)

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
        frame = pd.DataFrame(data)
        if k == 0:
            frame.to_csv('data_u.csv',encoding='utf-8',index=False)
        else :
            frame.to_csv('data_u.csv',mode = 'a+',header = False, encoding='utf-8',index=False)
    
        k = k+1
    f_index.close()
