import datetime
import pymysql
import config


db = pymysql.connect(host=config.D_host, user=config.D_user, passwd=config.D_passwd,
                     db=config.D_name, port=config.D_port, charset='utf8')
Find_sql = ''
today = datetime.datetime.now().strftime("%Y-%m-%d")


def FindData(Find_sql):
    cursor = db.cursor()
    Find_sql = "SELECT * FROM tw_bank where Time = '%s' " % (today)
    try:
        cursor.execute(Find_sql)
        results = cursor.fetchall()
        for row in results:
            Id = row[0]
            Time = row[1]
            Cur = row[2]
            Cash_s = row[3]
            Cash_b = row[4]
            Spot_s = row[5]
            Spot_b = row[6]
            print("Id: %s, Time: %s, Cur: %s, Cash_s: %s, Cash_b: %s, Spot_s: %s, Spot_b: %s" %
                  (Id, Time, Cur, Cash_s, Cash_b, Spot_s, Spot_b))
    except:
        print("Error: unable to fecth data")
    db.close()


FindData(Find_sql)
