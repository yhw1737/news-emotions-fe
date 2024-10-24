from fastapi import FastAPI
from api.routers import news_router

app = FastAPI(docs_url='/api/docs', openapi_url='/api/openapi.json')

# Include news router for endpoints
app.include_router(news_router.router)

@app.get("/api")
def read_root():
    return {"message": "Welcome to the news_emotions API"}
