from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute

from api import auth_router
from api.schemas import ErrorResponse
from config import PORT
from database.admin import init_admin
from database.session import engine, run_database


async def on_startup(app: FastAPI):
    init_admin(app=app, engine=engine)
    await run_database()

    yield

app = FastAPI(lifespan=on_startup, responses={
    400: {"model": ErrorResponse}
})
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        '*'
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/ping', response_class=Response)
async def ping():
    return Response(status_code=200)


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
async def home():
    return f'<div style="display: flex; width: 100vw; height: 100vh; justify-content: center; background-color: #F9F9F9; color: #03527E;"> <b style="margin-top:35vh">Welcome!</b> </div>'


def prettify_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            parts = route.path.lstrip('/').split('/')
            route.operation_id = parts[0] + \
                ''.join(part.capitalize() for part in parts[1:])


prettify_operation_ids(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, forwarded_allow_ips='*')
