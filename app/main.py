from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.api.routes import router

from app.core.database import init_db


app = FastAPI()

init_db()

app.include_router(router)


@app.exception_handler(HTTPException)
def http_exception_handler(_: Request, exc: HTTPException):
	return JSONResponse(
		status_code=exc.status_code,
		content={"detail": exc.detail},
	)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(_: Request, exc: RequestValidationError):
	return JSONResponse(
		status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
		content={
			"detail": "Invalid request payload.",
			"errors": exc.errors(),
		},
	)


@app.exception_handler(Exception)
def unhandled_exception_handler(_: Request, __: Exception):
	return JSONResponse(
		status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
		content={
			"detail": (
				"An unexpected error occurred while processing your request. "
				"Please try again later."
			)
		},
	)


# import os

# from groq import Groq



# print(chat_completion.choices[0].message.content)