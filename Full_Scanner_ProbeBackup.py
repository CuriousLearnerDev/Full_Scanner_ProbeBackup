#!/usr/bin/env python
'''
主程序
'''


import requests
import queue
import threading
import urllib.request
from urllib.parse import quote # urllib请求url里面带中文就会报错用这个抱住就可以了
import time
import random
from urllib.request import ProxyHandler, build_opener
import argparse


count = 1 # 记录请求多少次

schedule=1 # 文件数量
save = None #扫描结果保存开关

pl=0 # 记录批量扫描的数量

current_time_=time.strftime("%Y-%m-%d%H:%M:%S", time.localtime())
def picture_choice():
    i = random.choice(range(4))
    if i == 0:
        return banner_1
    elif i == 1:
        return banner_2
    elif i == 2:
        return banner_3
    elif i == 3:
        return banner_4


# 批量扫描
def Batch_scan(path):
    Batch=[]
    i = 1
    # 叫文件内容变成
    search_url=queue.Queue()
    thefile=open(path, encoding="UTF-8")

    # 统计有多少行
    while True:
        buffer = thefile.read(1024 * 8192)
        if not buffer:
            break
        i += buffer.count('\n')


    print(UseStyle(f"{'-'*20}文件一共有"+str(i)+f"条目标{'-'*20}",fore='yellow'))
    # 叫每一行内容都保存到search_url中
    for i in open(path, encoding="UTF-8"):
        Batch.append(i.rstrip())

    return Batch

# 读取字典文件内容
def Read_dictionary(path):
    global schedule

    # 叫文件内容变成
    search_url=queue.Queue()
    thefile=open(path, encoding="UTF-8")

    # 统计有多少行
    while True:
        buffer = thefile.read(1024 * 8192)
        if not buffer:
            break
        schedule += buffer.count('\n')

    print(UseStyle("文件一共有"+str(schedule)+"条",fore='yellow'))

    # 叫每一行内容都保存到search_url中
    for i in open(path, encoding="UTF-8"):
        search_url.put(i.rstrip())

    return search_url

STYLE = {   # 前景色
            'black'    : 30,   #  黑色
            'red'      : 31,   #  红色
            'green'    : 32,   #  绿色
            'yellow'   : 33,   #  黄色
            'blue'     : 34,   #  蓝色
            'purple'   : 35,   #  紫红色
            'cyan'     : 36,   #  青蓝色
            'white'    : 37,   #  白色
        }

def UseStyle(string, fore):

    return f"\033[1;{STYLE[fore]}m{string}\033[0m"


# 提取出来的结果保存起来
def Searchresults(results_IP):
    global save
    Searchresults_document = open(save, 'a')  # 打开文件写的方式
    Searchresults_document.write((results_IP+'\n'))  # 写入
    Searchresults_document.close()  # 关闭文件

def current_time():
    return UseStyle(time.strftime("[%Y-%m-%d_%H:%M:%S]: [*]", time.localtime()),fore='blue')


def banner():
    Author='\033[0;33m作者：w啥都学\033[0m'
    Blog='\033[0;33mBlog地址：www.zssnp.top\033[0m'
    #blbl = '\033[0;33m哔哩哔哩：https://space.bilibili.com/432899074\033[0m'
    github='\033[0;33mgithub项目地址：https://github.com/Zhao-sai-sai/Full-Scanner_ProbeBackup\033[0m'
    Frame=f'\033[0;33m {"—"*60}\033[0m'
    help="""\033[0;31m 本程序是一个Full_Scanner工具的子工具，Full_Scanner还在写
    本工具是一个备份扫描工具可以批量目标扫描 注意：默认是用的自己生成的常见站长常见的备份方式，也可以指定字典\033[0m"""

    picture_=choose_color_2(picture_choice())


    icon=f"""\n{Frame}\n{picture_}\n\n{Author}\n{Blog}\n{github}\n{Frame}\n{help}\n{Frame}                          """


    return  icon

def choose_color_2(cb):

    i = random.choice(range(4))

    if i == 0:
        return "\033[1;32m{}\033[0m".format(cb)
    elif i == 1:
        return "\033[1;31m{}\033[0m".format(cb)
    elif i == 2:
        return "\033[1;33m{}\033[0m".format(cb)
    elif i == 3:
        return "\033[1;36m{}\033[0m".format(cb)




# 单位换算
def covertFukeSize(size):

    size=int(size)

    kb = 1024
    mb = kb * 1024
    gb = mb * 1024
    tb = gb * 1024

    if size >= tb:
        return "%.1f TB" % float(size / tb)
    if size >= gb:
        return "%.1f GB" % float(size / gb)
    if size >= mb:
        return "%.1f MB" % float(size / mb)
    if size >= kb:
        return "%.1f KB" % float(size / kb)
    else:
        return '文件小于1kb'



def ask(url,url_exists):
    HeadersConfig = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    }
    global count
    global save

    while not url_exists.empty():
        searchurl=url_exists.get()


        #print(current_time() + f"进度: {count}/{schedule}", "\r", end='')
        try:

            print(current_time() +
                  f"进度: {count}/{schedule}","\r", end='')
            back = urllib.request.Request(url=url+quote(str(searchurl)),headers=HeadersConfig, method='GET')
            response = urllib.request.urlopen(back, timeout=7, )
            if response.status == 200:
                count += 1
                content = response.headers['content-length']
                content=covertFukeSize(content)
                print()
                print(current_time() + UseStyle(f"请求第[{str(schedule)}]这个备份文件存在：" +url+ searchurl+f'文件大小：{content}', fore='green'))

                if save != None:
                    Searchresults(url+searchurl+f'\t\t文件大小：{content}')
        except Exception as cw:
            if str(cw) in "HTTP Error 404: Not Found": # 报错404的
                count += 1
            if str(cw) in "<urlopen error [Errno 113] No route to host>": # 报错超时的
                print('\n目标未7响应时间超时了！')
                break




            # print(UseStyle(f'请求第[{str(schedule)}][*]这个地址不存在：',fore='yellow')+UseStyle(url+searchurl+'\t\t\t\t\t[*]'+"状态码："+str(e.code),fore='red'))
            #print("\r",current_time() + f"正在探测: {searchurl}"+ f"进度: {count}/{schedule}",  end='')

def Thread(url,url_exists,T):
    threadpool = []
    for _ in range(int(T)):
        Threads = threading.Thread(target=ask, args=(url,url_exists, ))
        threadpool.append(Threads)
    for th in threadpool:
        th.start()
    for th in threadpool:
        threading.Thread.join(th)

def splicing(url,url_s,segmentation,T):
    url_exists = queue.Queue()
    dictionary = ['index.php.txt',
                  'backup.zip',
                  'website.zip',
                  'web.zip',
                  'index.zip',
                  'wwwroot.zip',
                  'faisunzip.zip',
                  'wwwroot.rar',
                  'wwwroot.tar.gz',
                  'wwwroot.gz',
                  'wwwroot.sql.zip',
                  'back.zip',
                  'wwwroot.sql',
                  'www.zip',
                  'backup.zip',
                  'bbs.zip',
                  'www.tar.gz',
                  "我的.txt"]
    small = [chr(i) for i in range(97,123)] # a-z
    calltaxi = [chr(i) for i in range(97, 123)]  # A-Z
    number = [str(i) for i in range(0, 10)] # 0-9

    suffix = ['.zip',
              '.rar',
              '.tar.gz',
              '.sql.gz',
              '.7z',
              '.sql',
              '.tar.tgz',
              '.tar.bz2',
              '.gz',
              '.tar.xz',
              '.log.gz',
              '.log.bz2',
              '.log.xz',
              '.wim',
              '.lzh',
              '.bak',
              '.txt',
              '.old',
              '.jar',
              '.temp']

    for i in small:  # a-z
        for Extract_4 in suffix:
            url_exists.put(i+Extract_4)

    for i in calltaxi:  # A-Z
        for Extract_5 in suffix:
            url_exists.put(i + Extract_5)

    for i in number:  # 0-9
        for Extract_6 in suffix:
            url_exists.put(i + Extract_6)

    for Extract_1 in dictionary:# 默认字典
        url_exists.put(Extract_1)

    for i in suffix: # 分割拼接
        for Extract_2 in segmentation:
            url_exists.put(Extract_2+i)

    for Extract_3 in suffix:# 域名拼接
        url_exists.put(url_s+Extract_3)

    global schedule
    schedule = str((len(url_exists.queue)))

    Thread(url,url_exists,T)


def fix(url,T,document,save_):

    global save
    save=save_
    # 自动添加协议头
    if url.startswith('http://') or url.startswith('https://'):
        if 'http://' in url:
            http = 'http://'
        elif 'https://' in url:
            http = 'https://'
    else:
        try: # 判断目标是不是目标是不是https
            http='https://'
            url=http+url.strip()
            r = requests.get(url=url)
        except requests.exceptions.SSLError:
            http = 'http://'
            url=url.replace('https://', http)


    url_s = url.replace(http, '')
    if url[-1] != '/':
        url += '/' # 查看最后一个是否有/没有添加/

    if ':' in url_s:
        url_s=url_s.split(':')[0]
        segmentation=url_s.split('.')

    else:
        segmentation=url_s.split('.')
    if document==None:
        splicing(url,url_s,segmentation,T)
        return
    else:
        document_=Read_dictionary(document)
        print("使用的字典是"+document+"\n\n")
        Thread(url,document_,T)

banner_1 = r"""    
         ___     _ _     ___                            
        | __|  _| | |___/ __| __ __ _ _ _  _ _  ___ _ _ 
        | _| || | | |___\__ \/ _/ _` | ' \| ' \/ -_) '_|
        |_| \_,_|_|_|   |___/\__\__,_|_||_|_||_\___|_| 
"""

banner_2 = r'''

             _____                                               
        () |_       |\ |\    ()  _   _,               _  ,_  
          /| ||  |  |/ |/----/\ /   / |  /|/|  /|/|  |/ /  | 
         (/    \/|_/|_/|_/  /(_)\__/\/|_/ | |_/ | |_/|_/   |/
'''

banner_3 = """


         __|    | |       __|                              
         _||  | | |____|\__ \  _|  _` |   \    \   -_)  _| 
        _|\_,_|_|_|     ____/\__|\__,_|_| _|_| _|\___|_|  
"""

banner_4 = """


                 _       __                 
                |_  ||__(_  _ _.._ ._  _ ._ 
                ||_|||  __)(_(_|| || |(/_|
"""

# banner_1 = choose_color(banner_1, "yellow")
# banner_2 = choose_color(banner_2, "green")
# banner_3 = choose_color(banner_3, "red")
# banner_4 = choose_color(banner_4, "cyan")
# banner_5 = choose_color(banner_5, "cyan")


if __name__ == '__main__':
    print(banner())

    parser = argparse.ArgumentParser(description=UseStyle("警告：请勿用于非法用途！否则自行承担一切后果",'red'),
                                     usage=choose_color_2('python3 Full_Scanner_ProbeBackup.py  [目标] [其他参数]'))

    Active_collect_message = parser.add_argument_group(choose_color_2("参数"),
                                                       choose_color_2("下面是参数和参数的使用说明"))

    Active_collect_message.add_argument('-u','--url',
                                        dest='url',
                                        type=str,
                                        nargs='?',
                                        help=choose_color_2("指定扫描的目标，比如https://baidu.com/"))
    Active_collect_message.add_argument('-many',
                                        dest='many',
                                        type=str,
                                        nargs='?',
                                        help=choose_color_2("多个目标保存到一个文件里面进行批量扫描"))

    Active_collect_message.add_argument('-t','-thread',
                                        dest='thread',
                                        type=int,
                                        nargs='?',
                                        help=choose_color_2("指定线程默认是1"))
    Active_collect_message.add_argument('-d','-document',
                                        dest='document',
                                        type=str,
                                        nargs='?',
                                        help=choose_color_2("指定字典默认是自己生成"))
    Active_collect_message.add_argument('-o','-save',
                                        dest='save',
                                        type=str,
                                        nargs='?',
                                        help=choose_color_2("扫描出来的结果保存到位置"))


    args=parser.parse_args()

    if args.url !=None or args.many != None:
        if args.thread==None:
            args.thread=1
        # 是否批量扫描
        if args.many == None:
            print(choose_color_2("\n你输入的目标地址是: " +
                                 args.url +
                                 '\n线程数是：' +
                                 str(args.thread) +
                                 "\n使用自动生成字典扫描！"+
                                 f'\n\033[0;33m {"—" * 60}\033[0m'))

            fix(args.url,args.thread,args.document,args.save)
        else:
            #print(Batch_scan(args.many))
            Many_Batch=Batch_scan(args.many) # 批量扫描
            for url in Many_Batch:
                count = 1  # 记录请求多少次
                schedule =1 # 重置字典的数量
                pl += 1  # 记录批量扫描的数量
                print(choose_color_2(
                                     f"\n\n正在扫描：{url} 第{str(pl)}个目标"+
                                     f"\n线程数是：{str(args.thread)}"))
                fix(url,args.thread,args.document,args.save)