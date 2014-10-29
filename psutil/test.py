import psutil, time, sys

while True:
    try:
        print("CPU1% CPU2%:",psutil.cpu_percent(interval=0, percpu=True),"\r",end="")
        time.sleep(0.5)
    except KeyboardInterrupt:
        sys.exit(0)
