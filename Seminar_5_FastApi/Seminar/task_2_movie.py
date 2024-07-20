from enum import Enum

import uvicorn
from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

movies = []


class Genre(Enum):
    Horror = 'Ужасы'
    Comedy = 'Комедия'
    Action = 'Боевик'
    Melodrama = 'Мелодрама'
    Fantasy = 'Фэнтези'


class Movie(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Genre


class MovieIn(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Genre


@app.get('/movies/', response_model=list[Movie])
async def root():
    logger.info('Отработал GET запрос tasks')
    return movies


@app.post('/movies/', response_model=dict)
async def create_movie(new_movie: MovieIn):
    movies.append(Movie(id=len(movies) + 1,
                        title=new_movie.title,
                        description=new_movie.description,
                        genre=new_movie.genre))
    logger.info('Отработал POST запрос')


@app.get('/movies/{genre}', response_model=list[Movie])
async def get_movies(genre: Genre):
    result = []
    logger.info('Отработал GET запрос tasks')
    for movie in movies:
        if movie.genre == genre:
            result.append(movie)
    return result


if __name__ == '__main__':
    uvicorn.run(
        'task_2_movie:app',
        host='127.0.0.1',
        port=8080
    )
