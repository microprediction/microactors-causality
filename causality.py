import datetime as datetime
with open('timestamp.txt','a') as f:
   f.write(str(datetime.now())+'\n')
