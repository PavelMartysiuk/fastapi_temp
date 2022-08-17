from fastapi import Request
from pydantic import ValidationError
from starlette.responses import JSONResponse

from server.main import app


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Provided values not valid.", "metadata": f"{exc}"},
    )
