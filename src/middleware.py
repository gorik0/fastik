from fastapi import FastAPI, Request

import logging

from src.errors import UserForbidden


logger = logging.getLogger('uvicorn.access')
logger.disabled= True
def register_middl(app:FastAPI):


    @app.middleware("http")
    async def custom_logging(req:Request,call_next):
        resp = await call_next(req)
        print("HHEHHEHHEHEH")

        mess = f'{req.method} -- - - {req.url.path}'
        print(mess)
        return resp
    

    @app.middleware('http')
    async def author(req:Request,call_next):
        if not "Authorization" in req.headers:
            raise UserForbidden()
        return await call_next(req)