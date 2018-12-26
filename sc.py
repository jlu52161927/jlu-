# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 09:53:14 2018

@author: Y
"""

#coding：utf-8
print('抢课小程序 made by Y\n\n')
import requests
import json
import hashlib
import time
s = requests.session()
posturl = "http://uims.jlu.edu.cn/ntms/j_spring_security_check" #post data的url
scoreurl = "http://uims.jlu.edu.cn/ntms/service/res.do" #获取成绩的url
selectclassurl = "http://uims.jlu.edu.cn/ntms/action/select/select-lesson.do"
headers	= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko)    Chrome/64.0.3282.186 Safari/537.36',
                    'Connection':'keep-alive',
                    'Content-Type':'application/json',
                    'Host':'uims.jlu.edu.cn',
                    'Origin':'http://uims.jlu.edu.cn',
                    'Referer':'http://uims.jlu.edu.cn/ntms/index.do',
                    'X-Requested-With':'XMLHttpRequest'}
def login():
    user = input('请输入账号: ')
    psd = input('请输入密码: ')
    alp = 'UIMS' + user + psd
    alp = hashlib.md5(alp.encode(encoding='utf-8')).hexdigest()
    data = {
            'j_username':user,
            'j_password':alp,
            'mousePath':'PGwABPAgDNPDgDeRIADvTKgEBTMAEQTOAEhTOwE0TQAFDTQgFUSRQFlRRwF2RSAGIRSAGXRSQGoRTAG5RTgHIRUQHYRVAHpRVgH6QWQIKQXgIcPYAIsOaAI8NbgJOLeAJeLfgJvKhgKAJlQKRIoAKiHsAKyHuALDGvALUFvwLlFwAL0GwAMTGwgMaGwwMnGxQM3GyANIGzANYGzwNpG0gN6G2QOLG2wOaG3wOrG4AO9G4QPOG4gPjG4wPvG5gP+cDwKv'
        }
    while True:
        #ttime = time.strptime(requests.head('http://uims.jlu.edu.cn').headers['Date'][5:25])
        # print(ttime)
            try:
                c = s.post(posturl, data=data, timeout=15)  # post data
                global x
                x = c
                if c.url == 'http://uims.jlu.edu.cn/ntms/userLogin.jsp?reason=loginError':
                    print('大兄弟，密码错啦！')
                    user = input('请重新输入账号：')
                    psd = input('请重新输入密码：')
                    alp = 'UIMS' + user + psd
                    alp = hashlib.md5(alp.encode(encoding='utf-8')).hexdigest()
                    data = {
            'j_username':user,
            'j_password':alp,
            'mousePath':'PGwABPAgDNPDgDeRIADvTKgEBTMAEQTOAEhTOwE0TQAFDTQgFUSRQFlRRwF2RSAGIRSAGXRSQGoRTAG5RTgHIRUQHYRVAHpRVgH6QWQIKQXgIcPYAIsOaAI8NbgJOLeAJeLfgJvKhgKAJlQKRIoAKiHsAKyHuALDGvALUFvwLlFwAL0GwAMTGwgMaGwwMnGxQM3GyANIGzANYGzwNpG0gN6G2QOLG2wOaG3wOrG4AO9G4QPOG4gPjG4wPvG5gP+cDwKv'
            }
                else:
                    print('登陆成功！')
                    return 
            except:
                print("学校可能在为难你，正在重试。。。")
def getlist():
    #splanId需要自己更改
    Payload = json.dumps({"tag":"lessonSelectLogTcm@selectGlobalStore","branch":"quick","params":   {"splanId":940}})
    clist = s.post(scoreurl, headers = headers, data = Payload, cookies = s.cookies, timeout = 6) #获取捷选课列 表
    info = json.loads(clist.text)
    info = info['value']
    unchoosen_info = []
    for information in info:
        if information["selectTag"] == "N":
            unchoosen_info.append(information)
    return unchoosen_info

def selectclass ():
    while True:
        try:
            info = getlist()
        except:
            print ('出了点小问题，正在重试...')
            time.sleep(5)
        if (len(info) == 0):
            return
        for i in info:
            time.sleep(0.1)
            print('正在抢' + i['lessonSegment']['fullName'] + ',' + i['teachClassMaster']['lessonTeachers'][0]['teacher']['name'] + '!')
            try:
                c = json.loads(s.post(selectclassurl, headers = headers, timeout = 6, cookies = s.cookies, data = json.dumps({"lsltId":i['lsltId'],"opType":"Y"})).text)
                if (c['errno'] == 0):
                    print ('抢到' + i['lessonSegment']['fullName'] + ',' + i['teachClassMaster']['lessonTeachers'][0]['teacher']['name'] + '!')
            except:
                print ('出了点小问题，正在重试...')
                time.sleep(5)
           
        
        


def main():
    cnt = 0
    login()
    info = getlist()
    print('待选课程：')
    for i in info:
        print(i['lsltId'])
        print(i['lessonSegment']['fullName'] + ',' + i['teachClassMaster']['lessonTeachers'][0]['teacher']['name'])
    print('即将开始抢课')
    while True:
        try:
            ttime = requests.head('http://www.sogou.com').headers['Date'][5:25]
            ltime = time.strptime(ttime, "%d %b %Y %H:%M:%S")
            #choosetime需要改成相应的抢课时间
            choosetime = 2018*31536000 + 12*2592000 + 26*86400 + 3*3600 + 52*60 - 2
            if (ltime.tm_year*31536000+ltime.tm_mon*2592000+ltime.tm_mday*86400+ltime.tm_hour*3600+ltime.tm_min*60+ltime.tm_sec >= choosetime):
            #if (ltime.tm_mday > 26 or (ltime.tm_mday == 26 and ltime.tm_hour >= 0)):
                selectclass()
                return 
            cnt += 1
            time.sleep(1)
            if (cnt % 100 == 0):
                try:
                    getlist()
                except:
                    print ('出了点小问题，正在重试...')
        except:
            print('出了点小问题，正在重试...')
            time.sleep(2)
        

if __name__ == "__main__":
    main()
    print('抢课完成！')
    input()
