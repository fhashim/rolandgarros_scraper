import subprocess

from datetime import datetime
import time
while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    logs = open('logs.txt','a')
    logs.write('\nTask Started at '+str(now))
    # exec('TicketFinder.py')
    subprocess.call("TicketFinder.py", shell=True)
    now = datetime.now()
    end_time = now.strftime("%H:%M:%S")
    logs.write('\nTask Ended or halted at '+str(now))
    logs.close()
    time.sleep(900)


