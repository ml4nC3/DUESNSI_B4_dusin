import sqlite3
from sqlite3 import Error

create_table_classes = """CREATE TABLE IF NOT EXISTS `CLASSES` (
  `id_classe` VARCHAR(42),
  `libelle` VARCHAR(42),
  `niveau` VARCHAR(42),
  PRIMARY KEY (`id_classe`));"""

create_table_eleves = """CREATE TABLE IF NOT EXISTS `ELEVES` (
  `id_eleve` VARCHAR(42),
  `nom` VARCHAR(42),
  `prenom` VARCHAR(42),
  `id_classe` VARCHAR(42),
  PRIMARY KEY (`id_eleve`),
  FOREIGN KEY (`id_classe`) REFERENCES `CLASSES` (`id_classe`));"""

create_table_fichiers = """CREATE TABLE IF NOT EXISTS `FICHIERS` (
  `id_fichier` VARCHAR(42),
  `empreinte` VARCHAR(42),
  `date_depot` VARCHAR(42),
  `chemin` VARCHAR(42),
  `id_eleve` VARCHAR(42),
  PRIMARY KEY (`id_fichier`),
  FOREIGN KEY (`id_eleve`) REFERENCES `ELEVES` (`id_eleve`));"""

create_table_evaluations = """CREATE TABLE IF NOT EXISTS `EVALUATIONS` (
  `id_eval` VARCHAR(42),
  `date` VARCHAR(42),
  `criteres` VARCHAR(42),
  PRIMARY KEY (`id_eval`));"""

create_table_noter = """CREATE TABLE IF NOT EXISTS `NOTER` (
  `id_eleve` VARCHAR(42),
  `id_eval` VARCHAR(42),
  `note` VARCHAR(42),
  PRIMARY KEY (`id_eleve`, `id_eval`),
  FOREIGN KEY (`id_eval`) REFERENCES `EVALUATIONS` (`id_eval`),
  FOREIGN KEY (`id_eleve`) REFERENCES `ELEVES` (`id_eleve`));"""

requests = [
    create_table_classes,
    create_table_fichiers,
    create_table_eleves,
    create_table_noter,
    create_table_evaluations]


def database_init():
    conn = sqlite3.connect("dusin.db")

    for request in requests:
        # Exécution des requêtes
        try:
            c = conn.cursor()
            c.execute(request)
            conn.commit()
        except Error as e:
            print(e)
        finally:
            # conn.close()
            if c is not None:
                c.close()


if __name__ == "__main__":
    # execute only if run as a script
    database_init()
else:
    print("ERREUR !! Le fichier d'initialisation ne doit être exécuté qu'en tant que script.")