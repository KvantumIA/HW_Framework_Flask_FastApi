import uvicorn
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


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


if __name__ == '__main__':
    uvicorn.run(
        'task_2_HTML:app',
        host='127.0.0.1',
        port=8080
    )
