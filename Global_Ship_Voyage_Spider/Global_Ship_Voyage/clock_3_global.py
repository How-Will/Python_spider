from datetime import date, datetime

import time
import os 
from apscheduler.schedulers.background import BackgroundScheduler

def tick():
    print("tick ! the time is : %s" % datetime.now())
    os.system("python mystart.py")


if __name__ == "__main__":
    scheduler = BackgroundScheduler()

    # 每4个小时执行一次代码
    scheduler.add_job(tick, 'interval', minutes=240, start_date=datetime.now())

    scheduler.start()

    print("Press Ctrl + {0} to exit".format('Break' if os.name == 'nt' else 'C'))
    try:
        while True:
            time.sleep(3600)
            print(f"sleep! - {datetime.now()}")
    
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Exit The Job !")