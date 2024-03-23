# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 10:28:12 2023

@author: flomr
"""
import fonction_filtres as ff
import pymongo
import math

nb_series = len(ff.recuperer_noms_series())

def listes_des_series():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Test_SAE"]

    # Requête MongoDB 
    pipeline = [
        {
            '$project': {
                '_id': 0,
                'nom_serie': 1,
                'langue':1
            }
        }
    ]
    liste_series = list(db.Occurences_test.aggregate(pipeline))
    client.close()

    

    resultat = liste_series
    tableau = []
    
    for element in resultat:
        nom_serie = element['nom_serie']
        langue = element['langue']
        ligne = [nom_serie, langue]
        tableau.append(ligne)
    
    return tableau

def calcul_df(mot , langue ):
    # Connexion à la base de données MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Test_SAE"]

    # Requête MongoDB 
    pipeline = [

        {
            '$match': {
                f'Occurences.{mot}': {'$exists': 'True'} , "langue": langue
            }
        },
        {
            '$project': {
                '_id': 0,
                'nom_serie': 1,
                'Occurences': f'$Occurences.{mot}'
            }
        }
    ]
    
    nb_series = list(db.Occurences_test.aggregate(pipeline))
    client.close()
    return len(nb_series)





def recuperer_occureces_positives(langue, nom_serie):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Test_SAE"]

    pipeline = [
        {
            "$match": { "nom_serie": nom_serie , "langue" : langue }
        },
        {
            "$project": {
                "motsSup5": {
                    "$filter": {
                        "input": { "$objectToArray": "$Occurences" },
                        "as": "item",
                        "cond": { "$gt": ["$$item.v", 10] }
                    }
                }
            }
        }
    ]
    result = db.Occurences_test.aggregate(pipeline)

    tableau = []
    for doc in result:
        mots_sup_5 = doc["motsSup5"]
        for item in mots_sup_5:
            mot = item["k"]
            valeur_associee = item["v"]
            tableau.append([mot, valeur_associee])

    client.close()
    return tableau

liste_docs_traitement = listes_des_series()
for element in liste_docs_traitement:
    serie = element[0]
    langue = element[1]
    Liste_mots_Occ_cool = recuperer_occureces_positives(langue, serie)
    liste_des_tf_idf = {}
    for ligne in Liste_mots_Occ_cool :
        mot = ligne[0]
        TF = ligne[1]
        DF = calcul_df(mot, langue)
        IDF = math.log(nb_series / DF)
        TF_IDF = TF * IDF
        liste_des_tf_idf[mot] = TF_IDF
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["Test_SAE"]
    collection = database["liste_des_tf_idf_des_series_test_4"]
    data = {
        "nom_serie": serie,
        "TF_IDF": liste_des_tf_idf,
        "langue": langue
    }
    collection.insert_one(data)
    print("Insertion des TF-IDF de la série", serie, "en", langue, "réussie") 
    client.close()