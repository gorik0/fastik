from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response 
from typing import Callable,Any

class BookExc(Exception):
    pass



class UserForbidden(BookExc):
    pass


def create_exc_handler (initial_det: Any, status:int)-> Callable[[Request,Exception],JSONResponse]:
    async def exc_handler (r:Request,exc: BookExc):
        return JSONResponse(
            status_code=status,
            content= initial_det
        )

    return exc_handler