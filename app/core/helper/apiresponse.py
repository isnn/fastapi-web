from fastapi.responses import JSONResponse
from sqlmodel import SQLModel
from datetime import datetime
from typing import Any
import uuid

def success_response(data: Any, message: str = "Success"):
    """
    Generate a standardized success response.
    Automatically handles SQLModel objects, lists, and datetime serialization.
    """
    def serialize(obj):
        if isinstance(obj, SQLModel):  # Serialize SQLModel instances
            return {key: serialize(value) for key, value in obj.dict().items()}
        elif isinstance(obj, list):  # Serialize lists of objects
            return [serialize(item) for item in obj]
        elif isinstance(obj, datetime):  # Convert datetime to ISO format string
            return obj.isoformat()  # This converts datetime to string
        elif isinstance(obj, uuid.UUID):  # Convert UUID to string
            return str(obj) 
        return obj  # Leave other types as is

    return JSONResponse(
        status_code=200,
        content={
            "message": message,
            "data": serialize(data),
        },
    )
