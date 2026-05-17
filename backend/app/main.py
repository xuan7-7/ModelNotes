from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.api import documents, ai

app = FastAPI(title='ModelNotes API', version='0.1.0')

# CORS — 允许前端开发服务器跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(documents.router)
app.include_router(ai.router)


@app.on_event('startup')
def on_startup():
    init_db()


@app.get('/')
def root():
    return {'message': 'ModelNotes API'}
