# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 14:29:33 2023

@author: flomr
"""

import pymongo
from bson import ObjectId
import fonction_filtres as ff


# Extraction de la liste des séries (noms des dossiers contenant les fichiers audios)
liste_dossiers = ff.extraire_valeurs_json('liste_des_fichier.json')




# Établir une connexion à la base de données MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["Test_SAE"]
collection = database["mots_extraits_test_lem"]
sources_erreurs = []
# Parcourir les dossiers
for dossier in liste_dossiers:
    language = ""
    liste_fichiers = ff.list_files(dossier)

    # Parcourir les fichiers
    for fichier in liste_fichiers:
        # Détermination du type de fichier
        type_fichier = ff.determine_file_type(fichier)

        # Extraction des mots
        if type_fichier == 'ZIP':
            mots_filtres = ff.filtrage_mots_interdits_zip(fichier)
            # Préparer les données à insérer
            for nom_fichier, liste_mot_filtre in mots_filtres:
                if 'VF' in fichier or 'fr' in fichier :   
                        language = "Francais"
                        liste_mot_lem = ff.lemmatize_fr(liste_mot_filtre)
                elif 'VO' in fichier or 'eng' in fichier :   
                        language = "Anglais"
                        liste_mot_lem = ff.lemmatize_eng(liste_mot_filtre)
                data = {
                    "_id": ObjectId(),
                    "mots": liste_mot_lem,
                    "langue": language,
                    "nom_dossier": dossier,
                    "nom_fichier": nom_fichier
                }
                collection.insert_one(data)
            print("liste de mots du fichier " + fichier + " est insérée")
        elif type_fichier == 'SRT':
            if 'VF' in fichier or 'fr' in fichier :   
                    language = "Francais"
                    mots_filtres = ff.lemmatize_fr(ff.filtrage_mots_interdits(fichier))
            elif 'VO' in fichier or 'eng' in fichier :   
                    language = "Anglais"
                    mots_filtres = ff.lemmatize_eng(ff.filtrage_mots_interdits(fichier))
            # Préparer les données à insérer
            data = {
                "_id": ObjectId(),
                "mots": mots_filtres,
                "langue": language,
                "nom_dossier": dossier,
                "nom_fichier": fichier
            }
            collection.insert_one(data)
            print("liste de mots du fichier " + fichier + " est insérée")            
        else:
            sources_erreurs.append(fichier)
            print("Aucun mot filtré dans le fichier " + fichier)
# Fermer la connexion à la base de données
client.close()
print(sources_erreurs)