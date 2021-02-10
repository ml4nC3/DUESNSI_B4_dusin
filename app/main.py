from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from typing import List

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def accueil(request: Request):
    """
    Fonction qui traite la requête d'accès à la page racine du site Web
    :param request:
    :return: Page d'accueil au format HTML
    """
    # TODO : ajouter ici le code pour récupérer la liste d'élèves, classe etc..
    return templates.TemplateResponse("index.html", {'request': request})


@app.post("/remise", response_class=HTMLResponse)
async def eleve_id(request: Request, nom: str = Form(...), prenom: str = Form(...), classe: str = Form(...)):
    """
    Fonction qui traite la requête de connexion d'un élève à l'interface de dépot
    :param request: objet requete HTTP
    :param nom: Nom de famille de l'élève, en provenance du formulaire de la page ...
    :param prenom: prénom de l'élève, en provenance du formulaire de la page ...
    :param classe: classe de l'élève, en provenance du formulaire de la page ...
    :return: Page d'envoi des fichiers élèves au format HTML
    """
    if not os.path.exists(classe):
        os.mkdir(classe)
    if not os.path.exists(classe + '/' + prenom + '.' + nom):
        os.mkdir(classe + '/' + prenom + '.' + nom)

    # TODO : Ajouter ici le code pour écrire les fichiers envoyés ?

    # Préparation de la structure de donnée séparément afin d'améliorer la lisibilité du code
    data_eleve = {
        'nom': nom,
        'prenom': prenom,
        'classe': classe
    }
    return templates.TemplateResponse("remise.html", {'request': request, "data_eleve": data_eleve})


@app.post("/remise/validation", response_class=HTMLResponse)
async def remise_des_fichiers(request: Request, fichiers : List[UploadFile] = File(...)):
    # NL : pourquoi ne pas gérer la remise de fichier en même temps que le reste du formulaire ?
    # NL : pourquoi pas mais peut-être sur 2 pages distinctes (authentification puis remise des fichiers, ce serait pas mal)
    filenames = [fichier.filename for fichier in fichiers]
    liste_fichiers = filenames[0]
    for file in filenames[1:] : 
        liste_fichiers += ', ' + file
    return templates.TemplateResponse("validation.html",{'request':request,'liste_fichiers':liste_fichiers })


