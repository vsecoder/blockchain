from fastapi import FastAPI
from app.handlers import router as handlers_router


def dispatcher(context):
    app = FastAPI()
    app.include_router(router=handlers_router, prefix="/api")

    @app.get("/")
    async def root():
        return {
            "dispatcher": __name__,
            "start_time": context["start_time"],
        }

    return app
