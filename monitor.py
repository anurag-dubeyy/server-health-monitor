import sqlite3
from datetime import datetime 
import psutil
import requests
import time
import logging

logging.basicConfig(
    filename="monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

WEBSITES =  [
    "https://www.google.com",
    "https://www.github.com",
]

CPU_LIMIT = 80
RAM_LIMIT = 90
DISK_LIMIT = 85
DB_FILE = "monitor.db"

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
        message = f"{name} is high at {value}% (limit {limit}%)"
        print(f"WARNING: {message}")   
        logging.warning(message) 

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu REAL,
            ram REAL,
            disk REAL
        )"""
    )
    conn.commit()
    conn.close()

def save_reading(cpu, ram, disk):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO readings (timestamp, cpu, ram, disk) VALUES (?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cpu, ram, disk),
    )
    conn.commit()
    conn.close()

def main():
    cpu = get_cpu_usage()
    ram = get_ram_usage()
    disk = get_disk_usage()

    print("=== System Health ===")
    print(f"CPU: {cpu}%")
    print(f"RAM: {ram}%")
    print(f"Disk: {disk}%")
    logging.info(f"CPU={cpu}% RAM={ram}% Disk={disk}%")
    save_reading(cpu, ram, disk)

    check_limit("CPU", cpu, CPU_LIMIT)
    check_limit("RAM", ram, RAM_LIMIT)
    check_limit("Disk", disk, DISK_LIMIT)

    print("--- Websites ---")
    for site in WEBSITES:
        status = check_website(site)
        print(f"{site}: {status}")
        if status == "UP":
            logging.info(f"{site} is UP")
        else:
            logging.error(f"{site} is {status}")    

init_db()
while True:
    main()
    time.sleep(5)  
    
