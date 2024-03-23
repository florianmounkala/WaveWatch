# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 15:46:05 2023

@author: flomr
"""

import pymongo 
import fonction_filtres as ff

# Exemple d'utilisation / Tests



#Affichage des resultats 

liste_dossiers = ff.recuperer_noms_series()
langues_traduites = ["Anglais" , "Francais"]
compteur_erreur = 0
for dossier in liste_dossiers :
    for langue in langues_traduites :
        mots_documents = ff.recuperer_mots_documents(dossier , langue)
        liste_mots_filtre = ff.nettoyer_liste_mots(mots_documents , langue)
        documents_count = ff.compter_documents(dossier , langue)
        print ("le nombre d'episode en ", langue ," est de : ", documents_count)
        print("nombre de mots filtre :" , len(liste_mots_filtre))
        if documents_count == 0 or len(liste_mots_filtre) == 0 :
            print ( "echec insertion de la serie :", dossier , "en" , langue)    
        else: 
        
            occurences = ff.calculer_occurrences(liste_mots_filtre)
            
            print ("insertion des tf_idf de la serie " , dossier , " en ", langue , " reussie")        
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            database = client["Test_SAE"]
            collection = database["Occurences_lem2"]
            data = {
                "nom_serie": dossier,
                "Occurences": occurences,
                "langue": langue
            }
            try:
                collection.insert_one(data)
                print ("insertion des tf_idf de la serie " , dossier , " en ", langue , " reussie")            
            except ValueError as e:
                print("Erreur lors de l'insertion des données :", str(e))
                print ( "echec insertion de la serie :", dossier , "en" , langue)  
  
   



