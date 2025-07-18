from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .schemas import TicketCreate, TicketResponse
from threading import Lock

app = FastAPI(
    title="Anonymous Ticket Support API",
    description="Backend for submitting and managing anonymous support tickets. "
                "Provides in-memory ticket storage.",
    version="0.1.0",
    openapi_tags=[
        {"name": "Tickets", "description": "APIs for ticket management."}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    """Health check endpoint to verify the service is up."""
    return {"message": "Healthy"}

# In-memory "DB"
tickets = []
ticket_id_counter = 1
_db_lock = Lock()

# PUBLIC_INTERFACE
@app.post("/tickets", response_model=TicketResponse, status_code=201, tags=["Tickets"], summary="Create Ticket", description="Submit a new support ticket anonymously.")
def create_ticket(ticket: TicketCreate):
    """Creates a new support ticket anonymously.
    Args:
        ticket: TicketCreate - Subject and description of the issue.
    Returns:
        TicketResponse: The created ticket's details.
    """
    global ticket_id_counter
    with _db_lock:
        current_id = ticket_id_counter
        ticket_id_counter += 1
        ticket_data = {
            "id": current_id,
            "subject": ticket.subject,
            "description": ticket.description,
            "status": "open"
        }
        tickets.append(ticket_data)
    return ticket_data

# PUBLIC_INTERFACE
@app.get("/tickets", response_model=List[TicketResponse], tags=["Tickets"], summary="List Tickets", description="Retrieve all submitted tickets.")
def list_tickets():
    """Gets all submitted tickets (ordered by submission time)."""
    return tickets

# PUBLIC_INTERFACE
@app.get("/tickets/{ticket_id}", response_model=TicketResponse, tags=["Tickets"], summary="Get Ticket", description="View the details and status of a specific ticket by ID.")
def get_ticket(ticket_id: int):
    """Retrieves the details and status of a ticket with the given ID.
    Args:
        ticket_id (int): Ticket ID to retrieve.
    Returns:
        TicketResponse: Ticket info if it exists.
    Raises:
        HTTPException: If ticket is not found (404).
    """
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")
