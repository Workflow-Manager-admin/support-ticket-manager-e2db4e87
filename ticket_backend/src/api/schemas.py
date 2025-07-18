from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
class TicketCreate(BaseModel):
    """Schema for incoming ticket creation requests."""
    subject: str = Field(..., description="Brief summary of the issue.")
    description: str = Field(..., description="Detailed description of the issue.")

# PUBLIC_INTERFACE
class TicketResponse(BaseModel):
    """Schema for outputting ticket information."""
    id: int = Field(..., description="Ticket identifier.")
    subject: str = Field(..., description="Brief summary of the issue.")
    description: str = Field(..., description="Detailed description of the issue.")
    status: str = Field(..., description="Current status of the ticket.")
