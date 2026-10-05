import psutil
import requests
import time

WEBSITES =  [
    "https://www.google.com",
    "https://www.github.com",
]
CPU_LIMIT = 80
RAM_LIMIT = 90
DISK_LIMIT = 85

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    return psutil.virtual_memory().percent  

def get_disk_usage():
    return psutil.disk_usage("C:\\").percent

def check_website(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return "UP"
        return f"DOWN(status {response.status_code})"
    except requests.RequestException:
        return "DOWN (no response)"
def check_limit(name, value, limit):
    if value > limit:
        print(f"WARNING: {name} is high at {value}% (limit {limit}%)")    
def main():
    cpu = get_cpu_usage()
    ram = get_ram_usage()
    disk = get_disk_usage()
    print("=== System Health ===")
    print(f"CPU: {cpu}%")
    print(f"RAM: {ram}%")
    print(f"Disk: {disk}%")

    check_limit("CPU", cpu, CPU_LIMIT)
    check_limit("RAM", ram, RAM_LIMIT)
    check_limit("Disk", disk, DISK_LIMIT)

    print("--- Websites ---")
    for site in WEBSITES:
        print(f"{site}: {check_website(site)}")

while True:
    main()
    time.sleep(5)  
    
