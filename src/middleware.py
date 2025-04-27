from fastapi import FastAPI, Request


def register_middl(app:FastAPI):


    @app.middleware("http")
    async def custom_logging(req:Request,call_next):
        resp = await call_next(req)
        print("HHEHHEHHEHEH")
        return resp