from fastapi import FastAPI

app = FastAPI(
    title="Log Analytics API",
    version="0.1.0",
    description="API for ingesting, querying, and analyzing application logs."
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Log Analytics API is running"}