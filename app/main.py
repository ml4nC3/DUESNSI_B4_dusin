from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, pathlib, json
from typing import List
from dusindb import DusinDB

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/storage", StaticFiles(directory="storage"), name="storage")
templates = Jinja2Templates(directory="templates")

dusin_db = DusinDB()


@app.get("/", response_class=HTMLResponse)
async def accueil(request: Request):
    """
    Fonction qui traite la requête d'accès à la page racine du site Web
    :param request:
    :return: Page d'accueil au format HTML
    """
    # TODO : ajouter ici le code pour récupérer la liste d'élèves, classe etc..
    return templates.TemplateResponse("index.html", {'request': request})

chemin_dossier_a_completer = ""

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
    if not os.path.exists(classe + '/' + nom + '_' + prenom):
        os.mkdir(classe + '/' + nom + '_' + prenom)

    global chemin_dossier_a_completer

    chemin_dossier_a_completer = './' + classe + '/' + nom + '_' + prenom

    # Préparation de la structure de donnée séparément afin d'améliorer la lisibilité du code
    data_eleve = {
        'nom': nom,
        'prenom': prenom,
        'classe': classe
    }
    return templates.TemplateResponse("remise.html", {'request': request, "data_eleve": data_eleve})


@app.post("/remise/validation", response_class=HTMLResponse)
async def remise_des_fichiers(request: Request, fichiers : List[UploadFile] = File(...)):
    '''
    provoque une erreur si retour arrière et nouvelle remise (sans passer par la page login)
    '''
    liste_fichiers = ''
    for fichier in fichiers :
        content = await fichier.read()
        uploaded_file = open(chemin_dossier_a_completer + '/'+ fichier.filename, "wb")
        uploaded_file.write(content)
        uploaded_file.close()
        liste_fichiers += fichier.filename + ', '

    return templates.TemplateResponse("validation.html",{'request':request,'liste_fichiers':liste_fichiers })


@app.get("/prof", response_class=HTMLResponse)
async def ihm_correction(request: Request):
    # Pour récupérer l'extension d'un fichier : os.path.splitext(<path>), ou simplement str.split(".")

    fichiers = {
        "index.html": {"type": "html","path": "./storage/1_NSI/Bastien/index.html"},
        "styles.css": {"type": "css","path": "./storage/1_NSI/Bastien/styles.css"},
        "page1.html": {"type": "html","path": "./storage/1_NSI/Bastien/page1.html"}
        }

    for i, (fichier, f_attr) in enumerate(fichiers.items()):
        try:
            path = pathlib.Path(f_attr["path"])
            fichier_os = open(path, "r", encoding="utf8")
            f_attr["source"] = fichier_os.read()
        except:
            print("Erreur lecture fichier")
        finally:
            try:
                fichier_os.close()
            except:
                pass

    return templates.TemplateResponse("correction.html", {'request': request, "fichiers": fichiers, "json": json.dumps(fichiers)})