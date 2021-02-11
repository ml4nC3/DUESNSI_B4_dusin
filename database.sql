CREATE DATABASE IF NOT EXISTS `DUSIN` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `DUSIN`;

CREATE TABLE `CLASSE` (
  `id_classe` VARCHAR(42),
  `libelle` VARCHAR(42),
  `niveau` VARCHAR(42),
  PRIMARY KEY (`id_classe`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `FICHIERS` (
  `id_fichier` VARCHAR(42),
  `empreinte` VARCHAR(42),
  `date_depot` VARCHAR(42),
  `chemin` VARCHAR(42),
  `id_eleve` VARCHAR(42),
  PRIMARY KEY (`id_fichier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `ELEVE` (
  `id_eleve` VARCHAR(42),
  `nom` VARCHAR(42),
  `prenom` VARCHAR(42),
  `id_classe` VARCHAR(42),
  PRIMARY KEY (`id_eleve`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `NOTER` (
  `id_eleve` VARCHAR(42),
  `id_eval` VARCHAR(42),
  `note` VARCHAR(42),
  PRIMARY KEY (`id_eleve`, `id_eval`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `EVALUATION` (
  `id_eval` VARCHAR(42),
  `date` VARCHAR(42),
  `criteres` VARCHAR(42),
  PRIMARY KEY (`id_eval`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `FICHIERS` ADD FOREIGN KEY (`id_eleve`) REFERENCES `ELEVE` (`id_eleve`);
ALTER TABLE `ELEVE` ADD FOREIGN KEY (`id_classe`) REFERENCES `CLASSE` (`id_classe`);
ALTER TABLE `NOTER` ADD FOREIGN KEY (`id_eval`) REFERENCES `EVALUATION` (`id_eval`);
ALTER TABLE `NOTER` ADD FOREIGN KEY (`id_eleve`) REFERENCES `ELEVE` (`id_eleve`);
