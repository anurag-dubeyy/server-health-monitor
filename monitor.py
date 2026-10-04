import psutil
import requests
import time

WEBSITES =  [
    "https://www.google.com",
    "https://www.github.com",
    "https://thissitedoesnotexist12345.com",
]


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
def main():
    print("=== System Health ===")
    print(f"CPU: {get_cpu_usage()}%")
    print(f"RAM: {get_ram_usage()}%")
    print(f"Disk: {get_disk_usage()}%")

    print("--- Websites ---")
    for site in WEBSITES:
        print(f"{site}: {check_website(site)}")

while True:
    main()
    time.sleep(5)  
    
