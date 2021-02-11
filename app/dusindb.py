import sqlite3
from sqlite3 import Error


class DusinDB:
    def __init__(self):
        self.conn = sqlite3.connect("../app_db/dusin.db")

    def __select__(self, select_statement):
        #conn = sqlite3.connect("./app/expenses.db")
        try:
            c = self.conn.cursor()
            c.execute(select_statement)
            results = c.fetchall()
        except Error as e:
            print(e)
            return []
        finally:
            try:
                c.close()
            except NameError:
                pass
        return results

    def __insert__(self, insert_statement):
        #conn = sqlite3.connect("./app/expenses.db")
        try:
            c = self.conn.cursor()
            c.execute(insert_statement)
        except Error as e:
            print(e)
            return []
        finally:
            try:
                c.close()
            except NameError:
                pass
        return True

    def __del__(self):
        self.conn.close()

    def ajout_classe(self, classe: str) -> bool:
        # insert into 'classes' ('libelle','niveau' ) values(classe, "1" )
        pass

    def ajout_eleve(self, classe: str, nom: str, prenom: str) -> bool:
        # Récupérer l'ID de la classe
        # insert into 'eleves' ('id_classe','nom','prenom') values(???,nom,prenom)
        pass

    def ajout_fichier(self, chemin: str, nom: str, prenom: str) -> bool:
        # Récupérer l'ID de l'élève
        # insert into 'fichiers' ('chemin','id_eleve') values(chemin_fichier,????)
        pass

    def lire_fichiers(self) -> dict:
        pass

