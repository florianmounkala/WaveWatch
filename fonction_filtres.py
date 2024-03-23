# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 10:33:31 2023

@author: flomr
"""
"""importations """
import re
import json
import zipfile
import os
import math
import string
import pymongo
import spacy
import unicodedata
from langdetect import detect
from pymongo import MongoClient
from collections import defaultdict


nlp = spacy.load('fr_core_news_sm')
nlp_eng = spacy.load("en_core_web_sm")
""" fonctions """


#calcul de l'occurence
def calculer_occurrences(listes_mots):
    occurrences = defaultdict(int)
    
    for mots in listes_mots:
        for mot in mots:
             occurrences[mot] += 1
    
    return occurrences

# Calcul du TF-Idf
## Calcul du TF
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

## Calcul du TF-IDF

def calculer_tf_idf(mot , langue , nom_serie ) :
    nb_total_series = 127
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Test_SAE"]

    # Requête MongoDB 
    pipeline = [

        {
            '$match': {
                f'Occurences.{mot}': {'$exists': 'True'} , "langue": langue , "nom_serie" : nom_serie
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
    
    nb_series_avec_mot = list(db.Occurences_test.aggregate(pipeline))
    client.close()
    TF_IDF = 0
    if len(nb_series_avec_mot) == 1 :
        DF = calcul_df(mot, langue)
        TF = nb_series_avec_mot[0]['Occurences']
        IDF = 0
        IDF = math.log(nb_total_series/DF+1)
        TF_IDF = TF * IDF
    else:
        TF_IDF = None
    return TF_IDF


#Détection de la langue d'un texte
def detecter_langue(liste_mots):
    texte = ' '.join(liste_mots)
    langue_detectee = detect(texte)
    return langue_detectee

# Listage des fichiers préssent dans un dossier donné
def list_files(directory):
    files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files


#Fonction de filtrage SRT
def filtrage_mots_interdits(nom_fichier_srt):
    liste_filtre = []
    mots_extraits = extraire_mots_de_srt(nom_fichier_srt)
    for mot in mots_extraits:
        if filtrage(mot) is not None:
            liste_filtre.append(mot)
    return liste_filtre
        

#Fonction de filtrage ZIP
def filtrage_mots_interdits_zip(chemin_fichier_zip):
    liste_nom_fichier = obtenir_noms_fichiers_zip(chemin_fichier_zip)
    resultat = []
    for nom_fichier in liste_nom_fichier:
        liste_ligne = obtenir_mots_fichiers(chemin_fichier_zip, nom_fichier)
        liste_mot = convertisseur_phrase_mot(liste_ligne)
        liste_mot_filtre = []
        for mot in liste_mot:
            if filtrage(mot) is not None:
                liste_mot_filtre.append(mot)
        resultat.append((nom_fichier, liste_mot_filtre))
    return resultat

   
#Fonction de détermination du type de fichier
def determine_file_type(file_path):
    if file_path.endswith('.zip'):
        return 'ZIP'
    elif file_path.endswith('.srt'):
        return 'SRT'
    else:
        try:
            with zipfile.ZipFile(file_path) as zip_file:
                return 'ZIP'
        except zipfile.BadZipFile:
            return 'Unknown'
        
#Fonction d'extraction de fichier SRT
def extraire_mots_de_srt(nom_fichier_srt):
    mots = []
    try:
        with open(nom_fichier_srt, 'r', encoding="latin-1") as fichier:
            lignes = fichier.readlines()
            texte_sous_titres = ""

            for ligne in lignes:
                ligne = ligne.strip()
                if re.match(r'^\d+$', ligne):
                    continue  # Ignore les numéros de séquence
                elif ligne == "":
                    if texte_sous_titres:
                        mots += re.findall(r'\b\w+\b', texte_sous_titres, re.UNICODE)
                    texte_sous_titres = ""
                else:
                    texte_sous_titres += ligne + " "

            # Si le dernier sous-titre n'était pas suivi d'une ligne vide
            if texte_sous_titres:
                mots += re.findall(r'\b\w+\b', texte_sous_titres, re.UNICODE)

    except FileNotFoundError:
        print(f"Fichier {nom_fichier_srt} non trouvé.")
    return mots

#Détection des nombres présents dans un texte
def trouver_entier_dans_chaine(chaine):
    # Utilise une expression régulière pour trouver un entier dans la chaîne
    match = re.search(r'\d+', chaine)

    if match:
        return True  # Convertit la chaîne en entier
    else:
        # Si aucun entier n'est trouvé, renvoie None
        return False

#Extraction de valeurs d'un fichier JSON
def extraire_valeurs_json(fichier_json):
    try:
        with open(fichier_json, 'r' , encoding='latin-1') as fichier:
            donnees = json.load(fichier)

            def parcourir_donnees(data):
                if isinstance(data, dict):
                    for valeur in data.values():
                        parcourir_donnees(valeur)
                elif isinstance(data, list):
                    for item in data:
                        parcourir_donnees(item)
                else:
                    valeurs.append(data)

            valeurs = []
            parcourir_donnees(donnees)

        return valeurs
    except FileNotFoundError:
        print(f"Le fichier {fichier_json} n'a pas été trouvé.")
        return []
    except json.JSONDecodeError:
        print(f"Erreur de décodage JSON dans le fichier {fichier_json}.")
        return []

#Fonction de créeation de la liste des caractères sppéciaux    
def creer_liste_caracteres_sans_lettres():
    caracteres = string.printable
    lettres = string.ascii_letters

    caracteres_sans_lettres = [c for c in caracteres if c not in lettres]

    return caracteres_sans_lettres

#Définitiond des valeurs interdites
liste_mots_interdits = extraire_valeurs_json('stop_words.json')
liste_mots_interdits_fr = extraire_valeurs_json('mots-interdits.json')
liste_mots_interdits_eng =extraire_valeurs_json('stop_words_english.json')
liste_caracteres_sans_lettres = creer_liste_caracteres_sans_lettres()
liste_stop_words_eng = extraire_valeurs_json('liste-stop-words-anglais.json')
liste_stop_words_fr = extraire_valeurs_json('liste-stop-words-francais.json')

def filtrage_interne(liste_mot):
    liste_f = []
    for mot in liste_mot:
        liste_des_chiffres = ['1','2','3','4','5','6','7','8','9','0']
        mot_m = mot.lower() 
        mot_min = remove_accents(mot_m)
        for caracteres in liste_caracteres_sans_lettres :
            mot_min = mot_min.replace(caracteres , '')
        for chiffre in liste_des_chiffres :
           mot_min = mot_min.replace(chiffre , '') 
        if mot != None and mot_min != '' and len(mot_min)>1 and mot_min != None:
            liste_f.append(mot_min)
    return liste_f
# Fonction de Filtrage des listes de mots
def filtrage(mot):
    liste_des_chiffres = ['1','2','3','4','5','6','7','8','9','0']
    mot_m = mot.lower() 
    mot_min = remove_accents(mot_m)
    x =  0
    for caracteres in liste_caracteres_sans_lettres :
        mot_min = mot_min.replace(caracteres , '')
    
    for chiffre in liste_des_chiffres :
       mot_min = mot_min.replace(chiffre , '')    
    if trouver_entier_dans_chaine(mot_min) == True :
        x = x+1    
    if mot_min == '':
        x = x+1
    if mot_min in liste_mots_interdits :
        x = x+1
    if mot_min in liste_mots_interdits_fr :
        x = x+1
    if mot_min in liste_mots_interdits_eng :
        x = x+1
    if len(mot_min) < 3 :
        x = x+1
    if x == 0 and mot_min != " " :
        return mot_min

    
#Fonction d'obtention des nom des fichiers présents dans un zip
def obtenir_noms_fichiers_zip(chemin_zip):
    noms_fichiers = []
    with zipfile.ZipFile(chemin_zip, 'r') as fichier_zip:
        for nom_fichier in fichier_zip.namelist():
            noms_fichiers.append(nom_fichier)
    return noms_fichiers

#Fonction d'obtention du contenu des fichiers présents dans un zip
def obtenir_mots_fichiers(nom_zip , nom_fichier):
    nombre_de_lignes = 0
    lignes_de_texte = []
    try:
        with zipfile.ZipFile(nom_zip, mode="r") as archive:
            with archive.open(nom_fichier, mode="r") as hello:
                for line in hello:
                    ligne_texte = line.decode('latin-1').strip()
                    lignes_de_texte.append(ligne_texte)
                    nombre_de_lignes = nombre_de_lignes +1
        return (lignes_de_texte)                    
    except UnicodeDecodeError :
        print("erreur d'encodage avec le fichier"+ nom_zip + nom_fichier)
        return None
    
#Fonction de séparation des mmots
def convertisseur_phrase_mot(ligne_texte):
    mots = []    
    for phrase in ligne_texte:
        mots_phrase = phrase.split()
        mots.extend(mots_phrase)
    return mots


#### Partie Conversion 

#Fonction de suppression des mots inutiles
def nettoyer_liste_mots(listes_mots, langue):
    mots_propres = []  # Liste pour stocker les mots propres de chaque liste
    

    
    for mots_doc in listes_mots:
        mots_propres_doc = []  # Utilisation d'un ensemble pour éliminer les doublons
        
        for mot in mots_doc:
            mot = mot.lower()  # Convertir le mot en minuscules
            for caractere in liste_caracteres_sans_lettres:
                mot = mot.replace(caractere, '')
            mot = mot.replace('xx', '')
            mot = mot.replace('\x00', '')  # Supprimer les caractères restants
            if len(mot) > 2 and filtrage(mot) != None and filtrage(mot) != " ":
                mots_propres_doc.append(mot)
        
        mots_propres.append(list(mots_propres_doc))
    
    return mots_propres


#Récupération des mots 

def recuperer_mots_documents(nom_dossier , langue):
    # Connexion à la base de données MongoDB
    client = MongoClient('localhost', 27017)
    db = client['Test_SAE']
    collection = db['mots_extraits_test_lem']

    # Requête pour récupérer les documents par nom de dossier
    documents = collection.find({'nom_dossier': nom_dossier , 'langue' : langue})
 

    # Liste pour stocker tous les mots des documents
    mots_tous_documents = []

    # Itérer sur les documents et extraire les mots
    for document in documents:
        mots_document = document['mots']
        mots_tous_documents.extend(mots_document)

    return mots_tous_documents

def recuperer_noms_series_2():
    # Connexion à la base de données MongoDB
    client = MongoClient('localhost', 27017)
    db = client['Test_SAE']
    collection = db['liste_des_tf_idf_des_series_test_4']


    documents = collection.find()   

    # Liste pour stocker tous les mots des documents
    mots_tous_documents = []

    # Itérer sur les documents et extraire les mots
    for document in documents:
        mots_document = document['nom_serie']
        if mots_document not in mots_tous_documents:
            mots_tous_documents.append(mots_document)

    return mots_tous_documents

#Récupération des noms des séries
def recuperer_noms_series():
    # Connexion à la base de données MongoDB
    client = MongoClient('localhost', 27017)
    db = client['Test_SAE']
    collection = db['mots_extraits_test_lem']


    documents = collection.find()   

    # Liste pour stocker tous les mots des documents
    mots_tous_documents = []

    # Itérer sur les documents et extraire les mots
    for document in documents:
        mots_document = document['nom_dossier']
        if mots_document not in mots_tous_documents:
            mots_tous_documents.append(mots_document)

    return mots_tous_documents

#Calcul du nombre de d'episodes en une langue
def compter_documents(nom_dossier , langue):
    # Connexion à la base de données MongoDB
    client = MongoClient('localhost', 27017)
    db = client['Test_SAE']
    collection = db['mots_extraits_test_lem']
    compteur = 0
    # Requête pour récupérer les documents par nom de dossier
    if langue != "":
        documents = collection.find({'nom_dossier': nom_dossier , 'langue' : langue})
    else:
        documents = collection.find({'nom_dossier': nom_dossier})   
    # Itérer sur les documents et extraire les mots
    for document in documents:
        compteur = compteur +1
    return compteur




# Chargez le modèle de la langue française de spaCy
nlp = spacy.load('fr_core_news_sm')
##Francais



def lemmatize_fr(liste_word):
    liste_stemmed_word = []
    for word in liste_word :
        doc = nlp_eng(word)
        stemmed_word = doc[0].lemma_ if doc[0].lemma_ != "-PRON-" else word
        if len(stemmed_word)>1:
            liste_stemmed_word.append(stemmed_word)
    return liste_stemmed_word

def remove_accents(word):
    normalized_word = unicodedata.normalize('NFD', word)
    accent_removed = ''.join(c for c in normalized_word if not unicodedata.combining(c))
    
    accented_chars = "ÆæŒœ"
    unaccented_chars = "AEaeOeoe"

    for accented_char, unaccented_char in zip(accented_chars, unaccented_chars):
        if accented_char in accent_removed:
            accent_removed =  accent_removed.replace(accented_char, unaccented_char)
    
    return  accent_removed

def lemmatize_eng(list_word):
    list_lemmas = []
    for word in list_word :
        doc = nlp(word)
        lemmas = [token.lemma_ for token in doc]
        if len(lemmas)>1:
            list_lemmas.append(lemmas)
            
    return list_lemmas

########################################################

### PARITE MAIN ##############################"


def rechercher_tf_mot_query(mot , langue):
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
    
    result = list(db.liste_des_tf_idf_des_series_test_lem.aggregate(pipeline))
    # Fermeture de la connexion à la base de données
    client.close()
    return result

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

def est_nom_propre(mot):
    # Analyser le texte avec spaCy
    doc = nlp(mot)
    
    # Vérifier si le mot est une entité nommée
    if doc and doc[0].ent_type_ != '':
        return True
    else:
        return False
    
    
