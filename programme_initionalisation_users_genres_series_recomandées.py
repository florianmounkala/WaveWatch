# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:45:57 2023

@author: flomr
"""
### Importations 
from pymongo import MongoClient
import imdb
import fonction_filtres as ff 

client = MongoClient('localhost', 27017)
db = client['Test_SAE']

### Récupération des données des séries 

def recuperer_tf_idf_serie(nom_serie) :
    pipeline = {"nom_serie":nom_serie}
    result = list(db.liste_des_tf_idf_des_series_test_4.find(pipeline))
    tfidf_values = result[1]['TF_IDF']
    # Tri des valeurs de TF-IDF par ordre croissant
    sorted_tfidf = sorted(tfidf_values.items(), key=lambda x: x[1], reverse = True)
    client.close()
    return sorted_tfidf[:10]


### Insertion/ Association des genres a leur série 
# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['Test_SAE']
collection = db['liste_des_tf_idf_des_series_test_4']

series_sans_genres = []
liste_series = ff.recuperer_noms_series_2()
ia_counter = 0

for serie in liste_series:
    ia = imdb.IMDb()
    series = ia.search_movie(serie)
    
    if series:
        series_id = series[0].getID()
        detailed_series = ia.get_movie(series_id)
        
        if 'genres' in detailed_series:
            genres = detailed_series['genres']
            print('Genres de la série', serie, ':', genres)
            
            # Insérer les genres dans la base de données
            collection.update_many({'nom_serie': serie}, {'$set': {'genres': genres}}, upsert=True)
        else:
            print('Aucun genre trouvé pour la série', serie)
            series_sans_genres.append(serie)
    else:
        print('Aucune série correspondante trouvée.')
        series_sans_genres.append(serie)
    
    ia_counter += 1
    
    if ia_counter % 25 == 0:
        choix = input("Voulez-vous continuer ? (Oui/Non): ")
        if choix.lower() == "non":
            break

# Fermer la connexion à la base de données MongoDB
client.close()

### Ajout des séries recomandées 

# Se connecter à la base de données MongoDB

client = MongoClient('mongodb://localhost:27017')
db = client['Test_SAE']
collection = db['liste_des_tf_idf_des_series_test_4']

# Récupération de tous les documents de la collection
documents = collection.find()

# Parcours des documents et affichage de la variable TF-IDF
for document in documents:
    tf_idf = document.get("TF_IDF")
    nom_serie = document.get("nom_serie")
    langue = document.get("langue")
    mots_utiles = []
    if len(tf_idf) > 1 :
        # Trie le dictionnaire par valeur décroissante
        sorted_data = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)

        # Récupère les 10 premières clés
        top_50_keys = [key for key, value in sorted_data[:50]]
        # Affiche les 10 clés ayant les valeurs les plus élevées
        print("-" * 50)
        print("Les mots de la série : ", nom_serie ," en " ,langue," est de :")
        for mot in top_50_keys:
            if ff.est_nom_propre(mot):
                mots_utiles.append(mot)
        listes = []
        for mot in mots_utiles:
            query_result = ff.execute_query(mot, langue)
            listes.append(query_result)

        resultat_trouve = ff.additionner_tfidf(listes)
        liste_triee = ff.trier_par_tf_idf(resultat_trouve)
        if nom_serie in liste_triee  :
            liste_triee.remove(nom_serie)
        collection.update_one({'nom_serie': nom_serie , 'langue': langue}, {'$set': {'series_recomande': liste_triee}}, upsert=True)
            


# Fermeture de la connexion à la base de données
client.close()




