# main.py
from fastapi import FastAPI, Depends,Request,Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from fastapi.responses import JSONResponse,RedirectResponse
import  models
from fastapi.templating import Jinja2Templates 
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(

    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(SessionMiddleware, secret_key="some-random-string")


@app.get("/")
def read_names(request: Request):
    return 'Welcome to my project'

@app.get("/register/")
def read_names(request: Request,db: Session = Depends(get_db)):
    db_datas = db.query(models.Register).all()
    return templates.TemplateResponse('index.html', context={'request': request,'all':db_datas})

@app.get("/register/")
def read_names(request: Request,db: Session = Depends(get_db)):
    db_datas = db.query(models.Register).all()
    return templates.TemplateResponse('index.html', context={'request': request,'all':db_datas})

@app.post("/register/")
def add_name(request: Request,db: Session = Depends(get_db),name:str=Form(...)):
    db_register = models.Register(name=name)
    db.add(db_register)
    db.commit()
    db.refresh(db_register)
    return RedirectResponse(f'/register/',status_code=302)

@app.get("/register_get_id/{data}")
def add_name(request: Request,data:int,db: Session = Depends(get_db)):
    db_register = db.query(models.Register).filter(models.Register.id==data).first()
    print(db_register.name)
    response_data = jsonable_encoder({'Result':db_register})
    return JSONResponse(content=response_data,status_code=200)


@app.post("/edit_register/")
def add_name(request: Request,db: Session = Depends(get_db),editid:int=Form(...),editname:str=Form(...)):
    db.query(models.Register).filter(models.Register.id==editid).update({'name':editname})
    db.commit()
    return RedirectResponse(f'/register/',status_code=302)


@app.get("/delete_registery/{data}")
def add_name(request: Request,data:int,db: Session = Depends(get_db)):
    db_register = db.query(models.Register).filter(models.Register.id==data).first()
    db.delete(db_register)  
    db.commit()