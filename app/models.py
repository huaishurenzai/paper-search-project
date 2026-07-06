from pydantic import BaseModel

class PaperCreate(BaseModel):
    title: str
    authors: str
    year: int
    keywords: list[str]

class PaperUpdate(BaseModel):
    title: str
    authors: str
    year: int
    keywords: list[str]