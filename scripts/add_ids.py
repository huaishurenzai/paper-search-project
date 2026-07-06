import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "papers.json"
BACKUP_FILE = BASE_DIR / "data" / "papers_backup_before_add_id_run.json"

def main():
    if not DATA_FILE.exists():
        print("papers.json不存在")
        return
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        papers = json.load(f)

    if not isinstance(papers,list):
        print("papers.json最外层应该是列表")
        return

    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump(papers,f,ensure_ascii=False,indent=2)

    for index, paper in enumerate(papers,start=1):
        if "id" not in paper:
            paper["id"] = index

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(papers,f,ensure_ascii=False,indent=2)

    print(f"完成：已给{len(papers)}篇论文添加id")

if __name__ == "__main__":
    main()