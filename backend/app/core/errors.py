from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ProblemException(HTTPException):
    def __init__(self, status_code: int, title: str, detail: str, type_url: str = "about:blank") -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.title = title
        self.type_url = type_url


def _problem_response(request: Request, status_code: int, title: str, detail: str, type_url: str = "about:blank") -> JSONResponse:
    payload = {
        "type": type_url,
        "title": title,
        "status": status_code,
        "detail": detail,
        "instance": str(request.url.path),
    }
    return JSONResponse(payload, status_code=status_code, media_type="application/problem+json")


def register_problem_handlers(app: FastAPI) -> None:
    @app.exception_handler(ProblemException)
    async def handle_problem_exception(request: Request, exc: ProblemException) -> JSONResponse:
        return _problem_response(request, exc.status_code, exc.title, str(exc.detail), exc.type_url)

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        title = "HTTP Error"
        return _problem_response(request, exc.status_code, title, str(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(request: Request, exc: RequestValidationError) -> JSONResponse:
        return _problem_response(request, 422, "Validation Error", str(exc.errors()))
