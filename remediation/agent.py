import requests
import time
from actions import remediate
import logging
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M",
    handlers=[
        logging.FileHandler("auto_ops.log"),
        logging.StreamHandler()          # also print to terminal
    ]
)
logger = logging.getLogger(__name__)


API_URL= "http://localhost:8000"

while True:
    try:
        # get all the open tickets
        response = requests.get(f"{API_URL}/tickets")
        response.raise_for_status()
        tickets= response.json()

        for ticket_id, ticket in tickets.items():
            if ticket['status'] == "open":
                logger.info(f"Processing Ticket #{ticket_id}: {ticket['issue']} on {ticket['source']}")

                # try to auto-fix
                sucess, note = remediate(ticket)

                if sucess:
                    # Mark as resolved
                    requests.patch(
                        f"{API_URL}/tickets/{ticket_id}",
                        json={"status": "resolved", "resolution_note": note}
                    )
                    logger.info(f"Auto-resolved Ticket #{ticket_id}: {note}")
                else:
                    from triage.bot import triage_ticket
                    ai_diagnosis = triage_ticket(ticket["issue"], ticket["source"])
                    requests.patch(
                        f"{API_URL}/tickets/{ticket_id}",
                        json={"status": "needs_human", "resolution_note": f"AI Diagnosis: {ai_diagnosis}"}
                    )
                    logger.warning(
                        f"Escalated Ticket #{ticket_id} with AI triage — {ticket['issue']}\n{ai_diagnosis}"
                    )
    except requests.exceptions.ConnectionError:
        logger.error("Cannot reach API at %s - is uvicorn running?", API_URL)
    time.sleep(15)  # Check every 15 seconds