import requests
import json
import datetime
import pymysql
import config
from bs4 import BeautifulSoup


res = requests.get('http://rate.bot.com.tw/xrt?Lang=zh-TW')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')
# 抓取幣別
mydivs = soup.findAll(class_='hidden-phone print_show')
# cash rate。抓取現金匯率
cr = soup.findAll(class_='rate-content-cash text-right print_hide')
# Spot exchange rate。抓取即期匯率
ser = soup.findAll(class_='rate-content-sight text-right print_hide')

rate = []
In_sql = ''
Cr_sql = ''
Tr_sql = ''
t = datetime.datetime.now().strftime("%Y-%m-%d")
rate.append(t)
# 連接資料庫
db = pymysql.connect(host=config.D_host, user=config.D_user, passwd=config.D_passwd,
                     db=config.D_name, port=config.D_port, charset='utf8')


def Writejson(rate):
    with open('rate.json', 'w') as f:
        # 將 rate 編碼成 JSON字串符
        f.write(json.dumps(rate, ensure_ascii=False, indent=18))


def CreateTable(Cr_sql):
    cursor = db.cursor()
    Cr_sql = '''CREATE TABLE tw_bank(
            No INTEGER AUTO_INCREMENT PRIMARY KEY,
            Time varchar(50) NOT NULL,
            Cur char(50) NOT NULL,
            Cash_s float (50,4),
            Cash_b float (50,4),
            Spot_s float (50,4),
            Spot_b float (50,4))'''
    try:
        # 使用execute方法執行SQL語句
        cursor.execute(Cr_sql)
        # 提交指令
        db.commit()
        print('finsh')
    except:
        # 錯誤時，回復上一次正確狀態
        db.rollback
        print('Error')


def InsertData(In_sql):
    cursor = db.cursor()
    In_sql = '''INSERT INTO tw_bank(Time, Cur, Cash_s, Cash_b, Spot_s, Spot_b) \
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s')''' % \
        (t, curr, Cash_s, Cash_b, Spot_s, Spot_b)
    try:
        cursor.execute(In_sql)
        db.commit()
    except:
        db.rollback
        print('Error')


def TruncateTable(Tr_sql):
    cursor = db.cursor()
    Tr_sql = '''TRUNCATE TABLE tw_bank'''
    try:
        cursor.execute(Tr_sql)
        db.commit()
        print('finsh')
    except:
        db.rollback
        print('Error')


# CreateTable(Cr_sql)
# TruncateTable(Tr_sql)

for x in range(0, 19):
    curr = mydivs[x].text.strip()
    Cash_b = cr[x * 2].text.strip()
    Cash_s = cr[x * 2 + 1].text.strip()
    Spot_b = ser[x * 2].text.strip()
    Spot_s = ser[x * 2 + 1].text.strip()
    item = {'現金買入': Cash_b, '現金賣出': Cash_s,
            '即期買入': Spot_b, '即期賣出': Spot_s}
    cur = {'幣別': curr, '匯率類別': item}
    rate.append(cur)
    InsertData(In_sql)
# 關閉MySQL連線
db.close()

print(json.dumps(rate, ensure_ascii=False, indent=18))
Writejson(rate)
