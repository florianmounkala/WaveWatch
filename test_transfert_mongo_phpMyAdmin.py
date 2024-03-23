#-*- coding: utf-8 -*-
"""
Created on Tue Dec 26 16:28:23 2023

@author: flomr
"""

#Inportation des librairies
from pymongo import MongoClient
import fonction_filtres as ff
import mysql.connector
import json

#Récupération des données de la base mongo db
def recup_infos_series(serie_x, langue_x):
    client = MongoClient('localhost', 27017)
    db = client['Test_SAE']
    collection = db['liste_des_tf_idf_des_series_test_4']
    requete = {'nom_serie': serie_x, 'langue': langue_x}
    result = list(collection.find(requete))
    client.close()

    if len(result) > 0:
        document = result[0]  

        nom_serie = document.get('nom_serie')
        TF_IDF = document.get('TF_IDF')
        langue = document.get('langue')
        genres = document.get('genres')
        series_recomande = document.get('series_recomande')

        if nom_serie is None or nom_serie == '':
            nom_serie = None
        if TF_IDF is None or TF_IDF == '':
            TF_IDF = None
        if langue is None or langue == '':
            langue = None
        if genres is None or genres == '':
            genres = None
        if series_recomande is None or series_recomande == '':
            series_recomande = None

        return nom_serie, TF_IDF, langue, genres, series_recomande
    else:
        return None

#Insertion dans la base phpMyadmin 
def insert_data_into_tables( serie_nom, serie_tf_idf, serie_langue, serie_genres, serie_recomande):
    # Établir une connexion
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='20082003flo',
        database='saes5'
    )

    if conn.is_connected():
        print('Connexion réussie à la base de données.')

    # Créer un objet curseur pour exécuter des requêtes
    cursor = conn.cursor()
    
    #Effectuer l'insertion dans la table mot
    cles_mots = serie_tf_idf.keys()
    for cle_mot in cles_mots:
        count_query = "SELECT COUNT(*) FROM mots WHERE mot = %s AND langue = %s"
        cursor.execute(count_query, (cle_mot, serie_langue))
        occurences = cursor.fetchone()[0]
            
        # Vérification du nombre d'occurrences
        if occurences == 0:
            # Insertion du mot dans la table
            insert_query = "INSERT INTO mots (mot , langue) VALUES (%s, %s)"
            cursor.execute(insert_query, (cle_mot,serie_langue))
            conn.commit()
            print("Le mot '{}' a été inséré dans la base de données.".format(cle_mot))
    

    # Effectuer l'insertion dans la table serie
    genres_json = json.dumps(serie_genres)
    series_recomandes_json = json.dumps(serie_recomande)
    insert_query_series = "INSERT INTO series (nom_serie, langue, genres, series_recomandes) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query_series, (serie_nom,serie_langue, genres_json, series_recomandes_json))

    # Effectuer l'insertion dans la table mots_series        
    for cle, valeur in serie_tf_idf.items():
        insert_query_mots_series = "INSERT INTO mots_series (mot, nom_serie, langue, tf_idf) VALUES (%s,%s, %s, %s)"
        cursor.execute(insert_query_mots_series, (cle, serie_nom, serie_langue, valeur))

    # Valider la transaction
    conn.commit()

    # Afficher le nombre de lignes insérées pour chaque table
    print(f"{cursor.rowcount} ligne(s) insérée(s) dans la table nom_serie.")
    print(f"{cursor.rowcount} ligne(s) insérée(s) dans la table mots.")
    print(f"{cursor.rowcount} ligne(s) insérée(s) dans la table mots_series.")

    # Fermer le curseur et la connexion
    cursor.close()
    conn.close()
    
    
liste_serie = ff.recuperer_noms_series()
langues_possibles = ["Francais", "Anglais"]

for langue in langues_possibles:
    for serie in liste_serie:
        result = recup_infos_series(serie, langue)
        if result is None:
            print("La série n'existe pas.")
        else:
            serie_nom, serie_tf_idf, serie_langue, serie_genres, serie_recomande = result
            insert_data_into_tables(serie_nom, serie_tf_idf, serie_langue, serie_genres, serie_recomande)
            print("nom :", serie_nom," traitée")
    
