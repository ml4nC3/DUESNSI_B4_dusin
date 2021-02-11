import sqlite3
from sqlite3 import Error


class DusinDB:
    def __init__(self):
        self.conn = sqlite3.connect("./app_db/dusin.db")

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
            self.conn.commit()
        except Error as e:
            print("Erreur INSERT pour " + insert_statement)
            print(e)
            return False
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
        insert = f"INSERT INTO 'classes' ('libelle','niveau' ) values('{classe}', '1' )"
        return self.__insert__(insert)

    def ajout_eleve(self, classe: str, nom: str, prenom: str) -> bool:
        # Récupérer l'ID de la classe
        select = f"""SELECT id_classe FROM classes 
                     WHERE libelle LIKE '{classe}';"""
        result = self.__select__(select)
        if len(result) == 1:
            id_classe = result[0][0]
        else:
            return False
        # insert into 'eleves' ('id_classe','nom','prenom') values(???,nom,prenom)
        insert = f"INSERT INTO eleves('id_classe', 'nom', 'prenom') values({id_classe}, '{nom}', '{prenom}')"
        return self.__insert__(insert)

    def ajout_fichier(self, chemin: str, nom: str, prenom: str) -> bool:
        # Récupérer l'ID de l'élève
        select = f"""SELECT id_eleve FROM eleves 
                    WHERE nom LIKE '{nom}' 
                    AND prenom LIKE '{prenom}';"""
        result = self.__select__(select)
        # Le résutat doit normalement être unique. Si ce n'est pas le cas il y a un problème.
        if len(result) == 1:
            id_eleve = result[0][0]
        else:
            return False
        # insert into 'fichiers' ('chemin','id_eleve') values(chemin_fichier,????)
        insert = f"INSERT INTO 'fichiers' ('chemin','id_eleve') values('{chemin}',{id_eleve})"
        return self.__insert__(insert)

    def lire_fichiers(self) -> dict:
        pass

    def lire_classes(self) -> dict:
        pass