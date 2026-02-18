import requests
import time
from actions import remediate

API_URL= "http://localhost:8000"

while True:
    # get all the open tickets
    response = response.get(f"{API_URL}/tickets")
    tickets= response.json()

    for ticket_id, ticket in tickets.items():
        if ticket['status'] == "open":
            print(f"🔧 Processing Ticket #{ticket_id}: {ticket['issue']}")
            
            # try to auto-fix
            sucess = remediate(ticket)

            if sucess:
                # Mark as resolved
                print(f"Auto-resolved Ticket #{ticket_id}")
            else:
                print(f"Manual intervention needed for #{ticket_id}")
    
    time.sleep(15)  # Check every 15 seconds