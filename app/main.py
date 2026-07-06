from fastapi import FastAPI

from app.routers import papers

app = FastAPI(title="Paper Search API")

app.include_router(papers.router)

@app.get("/")
def root():
    return {"message":"paper search API"}