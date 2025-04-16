import uvicorn
from fastapi import FastAPI

from app.api import router as api_router
from app.config import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(api_router, prefix="/v1")


@app.get("/")
def health_check():
    return {"status": "healthy", "service": settings.APP_NAME, "version": "0.1.0"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=settings.APP_PORT, reload=settings.DEBUG
    )
