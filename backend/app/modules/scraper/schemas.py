

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


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
    max_pages: int = Field(default=5, ge=1, le=200) # ge = greater than or equal to, le = less than or equal to
    follow_links: bool = Field(default=True)

class ScrapeResponse(BaseModel):
    """ Response from the scrape endpoint """
    status: ScrapeStatus
    pages_scraped: int
    message: str
    started_at: datetime = Field(default_factory=datetime.now(timezone.utc))