

from datetime import datetime, timezone
from enum import Enum

from pydantic import Field


#? Enum in Python = same as enum in TS
# class ScrapeStatus(str, Enum) means values ARE strings
# so ScrapeStatus.PENDING == "pending" is True
class ScrapeStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ScrapedPage(BaseModel):
    """ Represents one scraped page - this is what gets stored in the vector DB later """
    url: str
    title: str
    content: str                       # cleaned text content
    metadata: dict = Field(            # extra info we'll use in RAG responses - Field() adds metadata - like Zod's .describe() or .min() in TS
        default_factory=dict           # default_factory=dict is like defaultValue: {}
    )
    scraped_at: datetime = Field(default_factory=datetime.now(timezone.utc))

class ScrapeRequest(BaseModel):
    """ Request body for triggering a scrape via API """
    url: str = Field()