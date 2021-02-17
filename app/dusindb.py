import sqlite3
from sqlite3 import Error


class DusinDB:
    def __init__(self):
        try:
            print("ouverture ./app_db/dusin.db")
            self.conn = sqlite3.connect("./app_db/dusin.db")
        except Error as e:
            print("ERREUR Ouverture BDD:")
            print(e)

    def __select__(self, select_statement):
        #conn = sqlite3.connect("./app/expenses.db")
        try:
            c = self.conn.cursor()
            print("BDD exécution : " + select_statement)
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
            print("BDD exécution : " + insert_statement)
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

    def __get_eleve_id(self,  nom: str, prenom: str) -> int:
        select = f"""SELECT id_eleve FROM eleves 
                    WHERE nom LIKE '{nom}' 
                    AND prenom LIKE '{prenom}';"""
        result = self.__select__(select)
        # Le résutat doit normalement être unique. Si ce n'est pas le cas il y a un problème.
        if len(result) == 1:
            id_eleve = result[0][0]
            return id_eleve
        else:
            return 0

    def ajout_classe(self, classe: str) -> bool:
        # insert into 'classes' ('libelle','niveau' ) values(classe, "1" )
        insert = f"INSERT INTO 'classes' ('libelle','niveau' ) values('{classe}', '1' )"
        return self.__insert__(insert)

    def ajout_eleve(self, classe: str, nom: str, prenom: str) -> bool:
        """
        Ajouter un élève dans la base de donnée.
        :param classe: libellé de la classe de l'élève
        :param nom: Nom de famille
        :param prenom: Prénom de famille
        :return: True si réussite, False sinon
        """
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
        """
        Ajouter un fichier dans la base de donnée
        :param chemin: chemin du fichier à partir de la racine du serveur
        :param nom: Nom de famille
        :param prenom: Prénom de famille
        :return: True si réussite, False sinon
        """
        # Récupérer l'ID de l'élève
        id_eleve = self.__get_eleve_id(nom, prenom)
        if id_eleve == 0:
            return False

        # insert into 'fichiers' ('chemin','id_eleve') values(chemin_fichier,????)
        insert = f"INSERT INTO 'fichiers' ('chemin','id_eleve') values('{chemin}',{id_eleve})"
        return self.__insert__(insert)

    def lire_fichiers(self, classe: str, nom: str, prenom: str) -> dict:
        # TODO : récupérer les fichiers d'un élève donné d'une évaluation donnée
        fichier = None

        # Récupérer l'ID de l'élève
        id_eleve = self.__get_eleve_id(nom, prenom)
        if id_eleve == 0:
            return {}

        # Récupérer la liste des fichiers correspondants
        select = f"""SELECT chemin FROM fichiers 
                     WHERE id_eleve = {id_eleve};"""
        result = self.__select__(select)
        # print("LOG ICI !!! (oui je sais c'est moche... mais bon, zut, ce sont des sprint de 20min")
        # print(result)

        # Convertir les résutlats dans le format pratique pour la page prof : dict(nom_fichier: dict(chemin, type)
        fichiers = dict()
        for line in result:
            fichier = line[0].split("/")[-1]
            type = line[0].split(".")[-1]
            fichiers[fichier] = {"type": type,"path": line[0]}

        return fichiers

    def lire_classes(self) -> dict:
        # TODO : écrire cette méthode afin de récupérer la liste des classes et remplacer le champ texte par une liste déroulante
        pass