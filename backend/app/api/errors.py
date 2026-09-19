from fastapi import Request
from fastapi.responses import JSONResponse

class MargDarshakException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

async def margdarshak_exception_handler(request: Request, exc: MargDarshakException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error": True},
    )
