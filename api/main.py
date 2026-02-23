from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
tickets = {}

class Ticket(BaseModel):
    issue: str
    source: str

class TicketUpdate(BaseModel):
    status: str
    resolution_note: str= ""

@app.post("/tickets")
async def create_ticket(ticket: Ticket):
    ticket_id = len(tickets) + 1
    tickets[ticket_id] = {
        "id":ticket_id,
        "issue":ticket.issue,
        "source":ticket.source,
        "status":"open",
        "created_at":datetime.now().isoformat(),
        "resolved_at": None,
        "resolution_note": ""
    }
    return {"ticket_id":ticket_id,"status":"created"}

@app.get("/tickets")
async def get_tickets():
    return tickets

@app.patch("/tickets/{ticket_id}")
async def update_ticket(ticket_id:int, update: TicketUpdate):
    if ticket_id not in tickets:
        raise HTTPException(status_code=404, detail="Ticket not found")
    tickets[ticket_id]["status"] = update.status
    tickets[ticket_id]["resolution_note"] = update.resolution_note
    tickets[ticket_id]["resolved_at"] = datetime.now().isoformat()

    return {"ticket_id":ticket_id, "status":update.status}
