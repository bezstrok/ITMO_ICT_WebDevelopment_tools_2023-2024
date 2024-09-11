from fastapi import FastAPI, responses

from . import config

app = FastAPI(
    docs_url="/",
    default_response_class=responses.ORJSONResponse,
    debug=True,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=config.api.host,
        port=config.api.port,
    )
