# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 16:25:44 2023

@author: flomr
"""

from pymongo import MongoClient

def execute_query(mot , langue):
    # Connexion à la base de données MongoDB
    client = MongoClient('localhost', 27017)
    db = client['Test_SAE']

    # Exécution de la requête et stockage du résultat dans une variable
    pipeline = [
        {
            '$match': {
                f'TF_IDF.{mot}': {'$exists': True},
                'langue': langue
            }
        },
        {
            '$project': {
                '_id': 0,
                'nom_serie': 1,
                'tf_idf': f'$TF_IDF.{mot}'
            }
        }
    ]
    
    result = list(db.liste_des_tf_idf_des_series_test_4.aggregate(pipeline))
    # Fermeture de la connexion à la base de données
    client.close()
    return result

def trier_par_tf_idf(liste):
    liste_triee = sorted(liste, key=lambda x: x['tf_idf_total'], reverse=True)
    top_5_series = liste_triee[:6]
    noms_series = [item['nom_serie'] for item in top_5_series]
    return noms_series

def additionner_tfidf(listes):
    serie_tfidf = {}
    
    for liste in listes:
        for item in liste:
            nom_serie = item['nom_serie']
            tfidf = item['tf_idf']  # Modifier la clé en fonction de votre besoin

            if nom_serie in serie_tfidf:
                serie_tfidf[nom_serie] += tfidf
            else:
                serie_tfidf[nom_serie] = tfidf
    
    liste_consolidée = [{'nom_serie': nom, 'tf_idf_total': tfidf} for nom, tfidf in serie_tfidf.items()]
    liste_consolidée = sorted(liste_consolidée, key=lambda x: x['tf_idf_total'], reverse=True)
    
    return liste_consolidée

# Demande à l'utilisateur de saisir un mot
mot_recherche = ["cars","gun"]
langue = "Anglais"
# Appel de la fonction avec le mot donné par l'utilisateur et affichage du résultat
listes = []
for mot in mot_recherche:
    query_result = execute_query(mot, langue)
    listes.append(query_result)

resultat_trouve = additionner_tfidf(listes)
liste_triee = trier_par_tf_idf(resultat_trouve)
for item in liste_triee:
    print(item)