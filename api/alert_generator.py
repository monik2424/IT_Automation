# api/alert_generator.py
import requests
import random
import time

ISSUES = [
    "High CPU usage (98%)",
    "Disk space critical (95% full)", 
    "Apache service down",
    "VPN connection timeout"
]

SOURCES = ["Server-A", "Server-B", "VPN-Gateway"]

while True:
    issue = random.choice(ISSUES)
    source = random.choice(SOURCES)
    
    response = requests.post("http://localhost:8000/tickets", 
                            json={"issue": issue, "source": source})
    print(f"✓ Created ticket: {response.json()}")
    
    time.sleep(random.randint(10, 30))  # Alert every 10-30 sec