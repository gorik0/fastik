from fastapi import FastAPI, Request

import logging

from src.errors import UserForbidden
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger('uvicorn.access')
logger.disabled= True
def register_middl(app:FastAPI):

    app.add_middleware(
                CORSMiddleware,
                allow_origins=["l"],
                allow_methods=["DELETE"],  # Restrict to GET only
                allow_headers=["s"],
            )
    @app.middleware("http")
    async def custom_logging(req:Request,call_next):
        print(req.headers.get("Origin"))
        resp = await call_next(req)
        print("HHEHHEHHEHEH")

        mess = f'{req.method} -- - - {req.url.path}'
        print(mess)
        return resp
   