from pydantic import BaseModel, Field

class PaperCreate(BaseModel):
    title: str = Field(min_length=1)
    authors: str = Field(min_length=1)
    year: int = Field(ge=1900, le=2026)
    keywords: list[str] = Field(min_length=1)

class PaperUpdate(BaseModel):
    title: str = Field(min_length=1)
    authors: str = Field(min_length=1)
    year: int = Field(ge=1900,le=2026)
    keywords: list[str] = Field(min_length=1)