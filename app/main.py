from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, pathlib, json
from typing import List
from app.dusindb import DusinDB

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
    if not os.path.exists('./storage/'+ classe):
        os.mkdir('./storage/'+ classe)
        dusin_db.ajout_classe(classe) 
    if not os.path.exists('./storage/'+ classe + '/' + nom + '_' + prenom):
        os.mkdir('./storage/'+ classe + '/' + nom + '_' + prenom)
        dusin_db.ajout_eleve(classe,nom,prenom)

    # Préparation de la structure de donnée séparément afin d'améliorer la lisibilité du code
    data_eleve = {
        'nom': nom,
        'prenom': prenom,
        'classe': classe
    }
    return templates.TemplateResponse("remise.html", {'request': request, "data_eleve": data_eleve})


@app.post("/remise/validation/{classe}/{nom}/{prenom}", response_class=HTMLResponse)
async def remise_des_fichiers(request: Request, classe : str, nom : str, prenom : str, fichiers : List[UploadFile] = File(...)) :
    '''
    provoque une erreur si retour arrière et nouvelle remise (sans passer par la page login)
    '''
    liste_fichiers = ''
    data_eleve = {'classe': classe,'nom': nom,'prenom': prenom}
    for fichier in fichiers :
        content = await fichier.read()
        chemin_fichier = './storage/' + data_eleve['classe'] + '/' + data_eleve['nom'] + '_' + data_eleve['prenom'] + '/'+ fichier.filename
        uploaded_file = open(chemin_fichier, "wb")
        uploaded_file.write(content)
        uploaded_file.close()
        liste_fichiers += fichier.filename + ', '
        dusin_db.ajout_fichier(chemin_fichier, data_eleve['nom'], data_eleve['prenom']) 

    return templates.TemplateResponse("validation.html",{'request':request,'liste_fichiers':liste_fichiers })

@app.get("/prof/correction/", response_class=HTMLResponse)
async def ihm_correction(request: Request, classe=str ,nom=str, prenom=str):
    # Pour récupérer l'extension d'un fichier : os.path.splitext(<path>), ou simplement str.split(".")

    fichiers = dusin_db.lire_fichiers(classe, nom, prenom)
    print(fichiers)

    data_jinja = dict()

    for i, (fichier, f_attr) in enumerate(fichiers.items()):
        try:
            path = pathlib.Path(f_attr["path"])
            fichier_os = open(path, "r", encoding="utf8")
            f_attr["source"] = fichier_os.read()

            path_jinja = "/".join(f_attr["path"].split("/")[2:])
            print(f_attr["path"])
            data_jinja[fichier] = {"path": path_jinja}
        except:
            print("Erreur lecture fichier")
        finally:
            try:
                fichier_os.close()
            except:
                pass
    print("Donnée JINJA: ")
    print(data_jinja)
    print(data_jinja['index.html']["path"])
    return templates.TemplateResponse("correction.html", {'request': request, "fichiers": data_jinja, "json": json.dumps(fichiers)})

@app.get("/prof", response_class=HTMLResponse)
async def selection_eleve(request: Request):
    return templates.TemplateResponse("selection.html",{'request':request })

# TODO : mettre à jour la liste des ifhciers dans le select du template correction