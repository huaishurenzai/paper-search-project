import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "papers.json"

def load_papers():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_papers(papers):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

def get_next_id(papers):
    if not papers:
        return 1
    max_id = max(paper.get("id",0) for paper in papers)
    return max_id+1