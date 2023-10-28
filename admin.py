# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario

app = FastAPI()

@app.get("/")
def saludar():
    return {"mensaje": "hola mundo"}

@app.get("/usuarios")
def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

@app.post("/usuarios")
def create_usuario(usuario_data: dict, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(**usuario_data)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

