from fastapi import FastAPI, responses

from . import config, endpoints

app = FastAPI(
    docs_url="/",
    default_response_class=responses.ORJSONResponse,
    debug=True,
)

app.include_router(endpoints.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=config.api.host,
        port=config.api.port,
    )
