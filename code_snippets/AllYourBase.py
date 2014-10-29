import time

message = 'All your base are belong to us'

for i in range(10):
    for i in range(1,len(message)+1):
        print('\r'+message[:i],end='')
        time.sleep(0.05)
    print('\n')
