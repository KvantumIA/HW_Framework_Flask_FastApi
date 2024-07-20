from fastapi.responses import HTMLResponse,JSONResponse
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="./Seminar_5_FastApi/Lecture/templates")


@app.get('/', response_class=HTMLResponse)
async def read_root():
    return '<h1>Hello World3</h1>'


@app.get('/message/', response_class=JSONResponse)
async def read_root():
    message = {'message': 'Hello World'}
    return JSONResponse(content=message, status_code=200)


@app.get("/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name: str):
    return templates.TemplateResponse("item.html", {"request": request, "name": name})
