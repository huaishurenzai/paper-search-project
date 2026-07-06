import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

DATA_FILE = Path("papers.json")

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

def load_papers():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def root():
    return {"message": "paper search api"}

@app.get("/papers")
def get_papers():
    papers = load_papers()
    return {"count": len(papers),"papers":papers}

@app.get("/papers/search")
def search_papers(keyword: str):
    papers = load_papers()
    results = []

    keyword = keyword.lower()

    for paper in papers:
        title = paper.get("title","").lower()
        authors = paper.get("authors","").lower()
        keywords = " ".join(paper.get("keywords",[])).lower()

        if keyword in title or keyword in authors or keyword in keywords:
            results.append(paper)

    return {"count": len(results),"results":results}

def save_papers(papers):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(papers,f,ensure_ascii=False,indent=2)

@app.post("/papers")
def create_paper(paper:PaperCreate):
    papers = load_papers()

    new_paper={
        "id": get_next_id(papers),
        "title": paper.title,
        "authors": paper.authors,
        "year": paper.year,
        "keywords": paper.keywords,
    }

    papers.append(new_paper)
    save_papers(papers)
    return {"message": "paper created", "paper": new_paper}

def get_next_id(papers):
    if not papers:
        return 1
    max_id = max(paper.get("id",0) for paper in papers)
    return max_id + 1

@app.get("/papers/{paper_id}")
def get_paper(paper_id: int):
    papers = load_papers()

    for paper in papers:
        if paper['id'] == paper_id:
            return paper

    raise HTTPException(status_code=404, detail="Paper not found")

@app.put("papers/{paper_id}")
def update_paper(paper_id: int, paper: PaperUpdate):
    papers = load_papers()

    for index, old_paper in enumerate(papers):
        if old_paper["id"] == paper_id:
            updated_paper = {
                "id": paper_id,
                "title": paper.title,
                "authors": paper.authors,
                "year": paper.year,
                "keywords": paper.keywords,
            }

            papers[index] = updated_paper
            save_papers(papers)

            return {"message": "paper updated","paper": updated_paper}

    raise HTTPException(status_code=404,detail="paper not found")

@app.detele("/papers/{paper_id}")
def delete_paper(paper_id: int):
    papers = load_papers()

    for index, paper in enumerate(papers):
        if paper["id"] == paper_id:
            deleted_paper = papers.pop(index)
            save_papers(papers)

            return {"message": "paper deteled", "paper": deleted_paper}

    raise HTTPException(status_code=404,detail="Paper not found")
