import psutil
import time

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    return psutil.virtual_memory().percent  

def get_disk_usage():
    return psutil.disk_usage("C:\\").percent

def main():
    print("=== System Health ===")
    print(f"CPU: {get_cpu_usage()}%")
    print(f"RAM: {get_ram_usage()}%")
    print(f"Disk: {get_disk_usage()}%")

while True:
    main()
    time.sleep(5)  
    
