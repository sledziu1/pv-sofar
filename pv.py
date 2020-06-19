import requests
import time
from MySQLdb import _mysql
from datetime import datetime
import pvCfg as cfg

db = False

def GetSofarData(data):
    response = 0
    trial = 0
    success = False

    while success == False and trial < cfg.sofarDataRetryCount:
        trial+=1
        try:
            response = requests.get(cfg.sofarUrl, auth=(cfg.sofarUser, cfg.sofarPass), timeout=cfg.sofarDataTimeout)
            found = 0
            for line in response.text.split('\r\n'):
                if line.startswith('var webdata_now_p'):
                    data['currentPower'] = line.split('"')[1]
                    found+=1
                if line.startswith('var webdata_today_e'):
                    data['dailyEnergy'] = line.split('"')[1]
                    found+=1
                if line.startswith('var webdata_total_e'):
                    data['totalEnergy'] = line.split('"')[1]
                    found+=1
            if found == 3:
                success = True
        except:
            time.sleep(cfg.sofarDataRetryDelay)
    return success
        
def MySqlAdd(data):
    global db
    x = "INSERT INTO `pv` (`measured`, `power`, `energyDay`, `energyTotal`) VALUES ('"+str(datetime.now())+"', '"+data['currentPower']+"', '"+data['dailyEnergy']+"', '"+data['totalEnergy']+"');"
    success = False
    trial = 0

    while success == False and trial < cfg.mysqlRetryCount:
        trial += 1
        try:
            if(db):
                print("already connected")
                pass
            else:
                db=_mysql.connect(host=cfg.mysqlHost,user=cfg.mysqlUser, passwd=cfg.mysqlPass, db=cfg.mysqlDbName, port=cfg.mysqlPort, connect_timeout=cfg.mysqlTimeout)

            db.query(x)
            success = True
        except:
            time.sleep(cfg.mysqlRetryDelay)
            print("mysql fail")
    return success

data = {}
sofarRet = GetSofarData(data)

if sofarRet == True:
    mysqlRet = MySqlAdd(data)

    if mysqlRet == False:
        #store data
        pass

    print("Power: "+data["currentPower"]+" W")
    print("Daily energy: "+data["dailyEnergy"]+" kWh")
    print("Total energy: "+data["totalEnergy"]+" kWh")
