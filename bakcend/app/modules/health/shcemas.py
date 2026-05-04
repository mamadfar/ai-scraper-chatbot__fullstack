"""
Pydantic models for the health module
"""

from pydantic import BaseModel, Field
from datetime import datetime, timezone

#? BaseModel = Pydantic's base class for all data schemas
# In TS: interface IHealthResponse { ... } but with runtime validation

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime

    #model_config controls serialization behavior, means convert json to python objects and vice versa
    model_config = {
        # serialize datetime as ISO string, not a Python datetime object
        "json_encoders": {datetime: lambda v: v.isoformat()}
    }

    class ErrorResponse(BaseModel):
        detail: str
        status_code: int

        # Field() adds metadata - like Zod's .describe() or .min() in TS
        timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))