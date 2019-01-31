from requests_html import HTMLSession as hs

def get_story(url):
    global f
    session=hs()
    r=session.get(url,headers=headers)
    r.html.encoding='GBK'
    title=list(r.html.find('title'))[0].text#获取小说标题
    nr=list(r.html.find('.nr_nr'))[0].text#获取小说内容
    nextpage=list(r.html.find('#pb_next'))[0].absolute_links#获取下一章节绝对链接
    nextpage=list(nextpage)[0]
    if(nr[0:10]=="_Middle();"):
        nr=nr[11:]
    if(nr[-14:]=='本章未完，点击下一页继续阅读'):
        nr=nr[:-15]
    print(title,r.url)
    f.write(title)
    f.write('\n\n')
    f.write(nr)
    f.write('\n\n')
    return nextpage

def search_story():
    global BOOKURL
    global BOOKNAME
    haveno=[]
    booklist=[]
    book_link = []
    bookname=input("请输入要查找的小说名:\n")
    session=hs()
    payload={'searchtype':'articlename','searchkey':bookname.encode('GBK'),'t_btnsearch':''}
    r=session.get(url,headers=headers,params=payload)
    haveno=list(r.html.find('.havno'))#haveno有值，则查找结果如果为空
    booklist=list(r.html.find('.list-item'))#booklist有值，则有多本查找结果
    while(True):
        if(haveno!=[] and booklist==[]):
            print('Sorry~！暂时没有搜索到您需要的内容！请重新输入')
            search_story()
            break
        elif(haveno==[] and booklist!=[]):
            i = 1
            print("查找到{}本小说".format(len(booklist)))
            for book in booklist:
                print(str(i), book.text, book.absolute_links)
                book_link.append(book.absolute_links)
                i += 1

            #search_story()
            while 1:
                num = int(input('请选择对应的需要下载的小说序号\n'))
                if num > len(booklist):
                    print("小说序号错误,请重新输入\n")
                    continue
                else:
                    break
            BOOKURL = str(book_link[num - 1])[2:-2]
            BOOKNAME = bookname
            break
        else:
            print("查找到结果，小说链接:",r.url)
            BOOKURL=r.url
            BOOKNAME=bookname
            break

global BOOKURL
global BOOKNAME
url='http://m.50zw.net/modules/article/waps.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/53.0.2907.99'
}

search_story()
print(BOOKURL)
chapterurl=BOOKURL.replace("book","chapters")
session=hs()
r=session.get(chapterurl,headers=headers)
ch1url=list(r.html.find('.even'))[0].absolute_links#获取第一章节绝对链接
ch1url=list(ch1url)[0]
global f
f=open(BOOKNAME+'.txt', 'a',encoding='gb18030',errors='ignore')
print("开始下载,每一章节都需要爬到，速度快不了，请等候。。。。\n")
nextpage=get_story(ch1url)
while(nextpage!=BOOKURL):
    nextpage=get_story(nextpage)
f.close