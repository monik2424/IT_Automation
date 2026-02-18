from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json
app = FastAPI()
tickets = {}

class Ticket(BaseModel):
    issue: str
    source: str

@app.post("/tickets")
async def create_ticket(ticket: Ticket):
    ticket_id = len(tickets) + 1
    tickets[ticket_id] = {
        "id":ticket_id,
        "issue":ticket.issue,
        "source":ticket.source,
        "status":"open",
        "created_at":datetime.now().isoformat()
    }
    return {"ticket_id":ticket_id,"status":"created"}

@app.get("/tickets")
async def get_tickets():
    return tickets
