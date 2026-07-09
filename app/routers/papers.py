from fastapi import APIRouter,HTTPException
from app.models import PaperCreate,PaperUpdate
from app.storage import load_papers,save_papers,get_next_id

router = APIRouter(prefix="/papers", tags=["papers"])

@router.get("")
def get_papers():
    papers = load_papers()
    return {"count": len(papers), "papers": papers}

@router.get("/search")
def search_papers(keyword: str):
    keyword = keyword.strip()
    if not keyword:
        raise HTTPException(status_code=400,detail="keyword cannot be empty")

    papers = load_papers()
    results = []

    keyword = keyword.lower()

    for paper in papers:
        title = paper.get("title", "").lower()
        authors = paper.get("authors", "").lower()
        keywords = " ".join(paper.get("keywords",[])).lower()

        if keyword in title or keyword in authors or keyword in keywords:
            results.append(paper)

    return {"count": len(results),"results": results}

@router.post("")
def create_paper(paper:PaperCreate):
    papers = load_papers()

    new_paper = {
        "id": get_next_id(papers),
        "title": paper.title,
        "authors": paper.authors,
        "year": paper.year,
        "keywords": paper.keywords,
    }
    papers.append(new_paper)
    save_papers(papers)

    return {"message": "paper created", "paper": new_paper}


@router.get("/{paper_id}")
def get_paper(paper_id: int):
    papers = load_papers()
    for paper in papers:
        if paper["id"] == paper_id:
            return paper

    raise HTTPException(status_code=404, detail="paper not found")

@router.put("/{paper_id}")
def update_paper(paper_id: int, paper: PaperUpdate):
    papers = load_papers()

    for index, old_paper in enumerate(papers):
        if old_paper["id"] == paper_id:
            updated_paper = {
                "id": paper_id,
                "title": paper.title,
                "authors": paper.authors,
                "year": paper.year,
                "keywords": paper.keywords
            }

            papers[index] = updated_paper
            save_papers(papers)
            return {"message": "paper updated", "paper": updated_paper}
    raise HTTPException(status_code=404,detail="paper not found")

@router.delete("/{paper_id}")
def delete_paper(paper_id: int):
    papers = load_papers()

    for index,paper in enumerate(papers):
        if paper["id"] == paper_id:
            deleted_paper = papers.pop(index)
            save_papers(papers)

            return {"message": "paper deleted","paper": deleted_paper}

    raise HTTPException(status_code=404,detail="paper not found")