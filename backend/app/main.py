from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from .api.endpoints import router
from .monetization.api import router as monetization_router
from .core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router)
app.include_router(monetization_router, prefix="/api/v1/monetization", tags=["monetization"])

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["app.models.models", "app.models.lead_models", "app.monetization.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "DarkWeb Intel API is running"}
