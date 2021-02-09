from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def affiche(request: Request):
    return templates.TemplateResponse("item.html",{'request':request})

@app.post("/", response_class=HTMLResponse)
async def eleve_id(request: Request, nom: str = Form(...), prenom: str = Form(...), classe: str = Form(...)):
    if not os.path.exists(classe):
        os.mkdir(classe)
    if not os.path.exists(classe + '/' + prenom + '.' + nom):
        os.mkdir(classe + '/' + prenom + '.' + nom)
    return templates.TemplateResponse("index.html",{'request':request, 'nom' : nom , 'prenom' : prenom, 'classe' : classe})

@app.post("/remise", response_class=HTMLResponse)
async def remise_fichier(fichier_1: UploadFile = File(...)):
    return {"filename": fichier_1.filename}
