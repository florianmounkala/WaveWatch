<?php
// En-têtes requis
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

// Afficher les erreurs PHP
error_reporting(E_ALL);
ini_set('display_errors', 1);
// Fonction pour se connecter à la base de donnees
function connectToDatabase() {  
    // Paramètres de connexion à la base de donnees
    $dsn = "mysql:host=localhost;dbname=saes5";
    $user = "root";
    $password = "20082003flo";

    try {
        // Connexion à la base de donnees avec PDO
        $conn = new PDO($dsn, $user, $password);

        // Configuration des options PDO
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        return $conn;
    } catch(PDOException $e) {
        // Gestion des erreurs PDO
        return null;
    }
}   
// Fonction pour véeriier si un utilisateur existe
function userExists($nom_user, $password) {
    // Connexion à la base de donnees
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Requête pour vérifier si un utilisateur existe
            $query = "SELECT COUNT(*) FROM utilisateurs WHERE nom_user = :nom_user AND mdp = :password";

            // Préparation de la requête
            $stmt = $conn->prepare($query);

            // Liaison des paramètres user_id et password
            $stmt->bindParam(':nom_user', $nom_user);
            $stmt->bindParam(':password', $password);

            // Exécution de la requête
            $stmt->execute();

            // Récupération du résultat
            $userExists = $stmt->fetchColumn();

            // Renvoyer le résultat
            return $userExists;
        } catch(PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la vérification de l\'existence de l\'utilisateur : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de donnees
            $conn = null;
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de donnees.');
    }
}
// Fonction pour recuperer les noms de serie depuis la base de donnees
function getAllSeriesNames() {
    // Connexion à la base de donnees
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Requête pour recuperer les noms de serie depuis la base de donnees
            $query = "SELECT DISTINCT nom_serie FROM series";

            // Execution de la requête
            $stmt = $conn->query($query);

            // Recuperation des resultats
            $seriesNames = $stmt->fetchAll(PDO::FETCH_COLUMN);

            // Renvoyer les noms de serie
            return $seriesNames;
        } catch(PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la recuperation des noms de serie : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de donnees
            $conn = null;
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de donnees.');
    }
}

function getSeriesInfoByName($nom_serie , $langue) {
    // Connexion à la base de donnees
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Requête pour recuperer les informations de la serie par nom_serie
            $query = "SELECT * FROM series WHERE nom_serie = :nom_serie AND langue = :langue";

            // Preparation de la requête
            $stmt = $conn->prepare($query);

            // Liaison du paramètre nom_serie
            $stmt->bindParam(':nom_serie', $nom_serie);
            $stmt->bindParam(':langue', $langue);
            // Execution de la requête
            $stmt->execute();

            // Recuperation des resultats
            $seriesInfo = $stmt->fetch(PDO::FETCH_ASSOC);

            // Renvoyer les informations de la serie
            return $seriesInfo;
        } catch(PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la recuperation des informations de la serie : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de donnees
            $conn = null;
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de donnees.');
    }
}

// Fonction pour recuperer les informations de l'utilisateur par user_id
function getUserInfo($user_name , $password) {
    // Connexion à la base de donnees
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Requête pour recuperer les informations de l'utilisateur par user_id
            $query = "SELECT id_user , nom_user , mdp , email FROM utilisateurs WHERE nom_user = :user_name AND mdp = :password";

            // Preparation de la requête
            $stmt = $conn->prepare($query);

            // Liaison du paramètre user_id
            $stmt->bindParam(':user_name', $user_name);
            $stmt->bindParam(':password', $password);


            // Execution de la requête
            $stmt->execute();

            // Recuperation des resultats
            $userInfo = $stmt->fetch(PDO::FETCH_ASSOC);

            // Renvoyer les informations de l'utilisateur
            return $userInfo;
        } catch(PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la recuperation des informations de l\'utilisateur : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de donnees
            $conn = null;
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de donnees.');
    }
}
// Fonction pour recuperer les series likees de l'utilisateur
function getSeriesLikes($user_name , $password) {
    // Connexion à la base de donnees
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Requête pour recuperer les series likees de l'utilisateur
            $query1 = "SELECT series_likes FROM utilisateurs WHERE nom_user = :user_name AND mdp = :password";
            $stmt1 = $conn->prepare($query1);
            $stmt1->bindParam(':user_name', $user_name);
            $stmt1->bindParam(':password', $password);
            $stmt1->execute();
            $userLikes = $stmt1->fetch(PDO::FETCH_ASSOC)['series_likes'];

            // Si l'utilisateur n'a pas de series likees, ne rien renvoyer
            if (!$userLikes) {
                return null;
            }else{
                // Separer les series likees en un tableau
                $seriesLikees = explode(',', $userLikes);
                return $seriesLikees;
            }
            
        } catch(PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la recuperation des series likees de l\'utilisateur : ' . $e->getMessage());
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de donnees.');
    }
}

// Fonctions de récupération des séries recommandées d'un utilisateur
function removeSpecialCharacters($array) {
    $result = array();

    foreach ($array as $item) {
        // Supprimer les caractères "\", "[", et "]"
        $cleanedItem = str_replace(['\\', '[', ']', '"'], '', $item);
        $result[] = $cleanedItem;
    }

    return $result;
}
function getRecos($user_name , $password, $langue) {
    // Connexion à la base de données
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Récupérer les séries likées de l'utilisateur
            $seriesLikees = removeSpecialCharacters(getSeriesLikes($user_name , $password));

            // Si l'utilisateur n'a pas de séries likées, ne rien renvoyer
            if (empty($seriesLikees)) {
                return null;
            } else {
                // Tableau pour stocker les séries recommandées
                $seriesRecommandees = [];

                foreach ($seriesLikees as $seriesLikee) {
                    // Requête pour récupérer les séries recommandées
                    $query = "SELECT series_recomandes FROM series WHERE nom_serie = :nom_serie AND langue = :langue";

                    // Préparation de la requête
                    $stmt = $conn->prepare($query);

                    // Liaison des paramètres nom_serie et langue
                    $stmt->bindParam(':nom_serie', $seriesLikee);
                    $stmt->bindParam(':langue', $langue);

                    // Exécution de la requête
                    $stmt->execute();

                    // Récupération du résultat
                    $seriesRecomandes = $stmt->fetchColumn();

                    // Ajouter la valeur series_recomandes au tableau des séries recommandées
                    $seriesRecommandees[] = $seriesRecomandes;
                }

                // Renvoyer les valeurs series_recomandes des séries recommandées
                return $seriesRecommandees;
            }
        } catch (PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la récupération des séries recommandées : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de données
            $conn = null;
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de données.');
    }
}
function splitStringsIntoWords($array) {
    $splitArrays = array_map(function($item) {
        return explode(", ", $item);
    }, $array);

    $result = array_merge(...$splitArrays);

    return $result;
}
function sortByOccurrence($array) {
    $wordCounts = array_count_values($array);
    arsort($wordCounts);
    return array_keys($wordCounts);
}

function getSeriesLike($user_id) {
    // Connexion à la base de donnees
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Requête pour recuperer les series likees de l'utilisateur
            $query1 = "SELECT series_likes FROM utilisateurs WHERE id_user = :user_id";
            $stmt1 = $conn->prepare($query1);
            $stmt1->bindParam(':user_id', $user_id);
            $stmt1->execute();
            $userLikes = $stmt1->fetch(PDO::FETCH_ASSOC)['series_likes'];

            // Si l'utilisateur n'a pas de series likees, ne rien renvoyer
            if (!$userLikes) {
                return null;
            }else{
                // Separer les series likees en un tableau
                $seriesLikees = explode(',', $userLikes);

                // Supprimer les caractères spéciaux
                $result = array();
                foreach ($seriesLikees as $item) {
                    // Supprimer les caractères "\", "[", et "]"
                    $cleanedItem = str_replace(['\\', '[', ']', '"'], '', $item);
                    $result[] = $cleanedItem;
                }

                return $result;
            }
            
        } catch(PDOException $e) {
            // Gestion des erreurs PDO
            return json_encode(['error' => 'Erreur lors de la recuperation des series likees de l\'utilisateur : ' . $e->getMessage()]);
        }
    } else {
        return json_encode(['error' => 'Erreur de connexion à la base de donnees.']);
    }
}
function removeElementsFromList($list1, $list2) {
    // Utiliser array_diff pour supprimer de $list2 tous les éléments présents dans $list1
    $result = array_diff($list2, $list1);

    // Renvoyer le résultat
    return $result;
}
// Fonctions de récupération des séries d'un genre donnée
function getGenres($genre , $langue) {
    // Connexion à la base de données
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Requête pour récupérer les séries d'un genre donné
            $query = "SELECT nom_serie FROM series WHERE genres LIKE CONCAT('%', :genre, '%') AND langue = :langue";

            // Préparation de la requête
            $stmt = $conn->prepare($query);

            // Liaison du paramètre genre
            $stmt->bindParam(':genre', $genre);
            $stmt->bindParam(':langue', $langue);

            // Exécution de la requête
            $stmt->execute();

            // Récupération des résultats
            $series = $stmt->fetchAll(PDO::FETCH_COLUMN);

            // Renvoyer les séries
            return $series;
        } catch (PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la récupération des séries : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de données
            $conn = null;
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de données.');
    }
}

//Fonction de recherche d'une serie par nom
function searchSeriesByName($nom_serie) {
    // Connexion à la base de données
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Requête pour récupérer les séries d'un genre donné
            $query = "SELECT nom_serie FROM series WHERE nom_serie LIKE CONCAT('%', :nom_serie, '%')";

            // Préparation de la requête
            $stmt = $conn->prepare($query);

            // Liaison du paramètre genre
            $stmt->bindParam(':nom_serie', $nom_serie);

            // Exécution de la requête
            $stmt->execute();

            // Récupération des résultats
            $series = $stmt->fetchAll(PDO::FETCH_COLUMN);

            // Renvoyer les séries
            return $series;
        } catch (PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la récupération des séries : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de données
            $conn = null;
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de données.');
    }
}
// Fonction de recherche d'une série a partir d'un mot clé
function ResearchByTFIDF($mot_cle , $langue) {
    // Connexion à la base de données
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Encodage du mot clé en UTF-8
            $mot_cle = mb_convert_encoding($mot_cle, 'UTF-8', mb_detect_encoding($mot_cle));

            // Requête pour récupérer les séries d'un genre donné
            $query = "SELECT nom_serie , tf_idf FROM mots_series  WHERE mot = :mot_cle AND langue = :langue Order by tf_idf DESC LIMIT 50";
            
            // Préparation de la requête
            $stmt = $conn->prepare($query);

            // Liaison du paramètre genre
            $stmt->bindParam(':mot_cle', $mot_cle);
            $stmt->bindParam(':langue', $langue);
            // Exécution de la requête
            $stmt->execute();
            if ($stmt->errorCode() != 0) {
                $errors = $stmt->errorInfo();
                echo($errors[2]);
            }

            // Récupération des résultats
            $series = $stmt->fetchAll(PDO::FETCH_ASSOC);
            if ($series == null) {
                // Requête pour récupérer les séries d'un genre donné
                $query = "SELECT nom_serie, tf_idf FROM mots_series WHERE mot LIKE CONCAT('%', :mot_cle, '%') and langue = :langue Order by tf_idf DESC LIMIT 10";

                // Préparation de la requête
                $stmt = $conn->prepare($query);

                // Liaison du paramètre genre
                $stmt->bindParam(':mot_cle', $mot_cle);
                $stmt->bindParam(':langue', $langue);

                // Exécution de la requête
                $stmt->execute();
                if ($stmt->errorCode() != 0) {
                    $errors = $stmt->errorInfo();
                    echo($errors[2]);
                }

                // Récupération des résultats
                $series = $stmt->fetchAll(PDO::FETCH_ASSOC);

                // Renvoyer les séries
                return array('series' => $series, 'message' => "mot cle non trouve");
            } else {
                return array('series' => $series, 'message' => "mot cle trouve");
            }

        } catch (PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la récupération des séries : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de données
            $conn = null;
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de données.');
    }
}

function searchByPhrase($phrase, $langue) {
    // Divisez la phrase en mots en utilisant les caractères de séparation spécifiés
    $mots = preg_split('/[;.,\s]+/', $phrase);

    // Créez un tableau pour stocker les résultats
    $resultats = array();

    // Exécutez la fonction ResearchByTFIDF pour chaque mot
    foreach ($mots as $mot) {
        $resultat = ResearchByTFIDF($mot, $langue);
        // Ajoutez le résultat au tableau de résultats
        foreach ($resultat['series'] as $serie) {
            if (!isset($resultats[$serie['nom_serie']])) {
                $resultats[$serie['nom_serie']] = array('count' => 1, 'tfidf' => $serie['tf_idf']);
            } else {
                $resultats[$serie['nom_serie']]['count']++;
                $resultats[$serie['nom_serie']]['tfidf'] += $serie['tf_idf'];
            }
        }
    }

    // Trier les résultats
    uasort($resultats, function($a, $b) {
        if ($a['count'] == $b['count']) {
            return $b['tfidf'] <=> $a['tfidf'];
        }
        return $b['count'] <=> $a['count'];
    });

    // Retournez uniquement les noms des séries
    return array_keys($resultats);
}
//Fonction Ajout Utilisateur
function AddUser($user_id, $user_name, $user_email, $user_password, $series_likes) {
    // Connexion à la base de données
    $conn = connectToDatabase();
    if ($conn) {
        try {
            // Requête pour ajouter un utilisateur
            $query = "INSERT INTO utilisateurs (id_user, nom_user, email, mdp, series_likes) VALUES (:user_id, :user_name, :user_email, :user_password, :series_likes)";

            // Préparation de la requête
            $stmt = $conn->prepare($query);

            // Liaison des paramètres
            $stmt->bindParam(':user_id', $user_id);
            $stmt->bindParam(':user_name', $user_name);
            $stmt->bindParam(':user_email', $user_email);
            $stmt->bindParam(':user_password', $user_password);
            $stmt->bindParam(':series_likes', $series_likes);

            // Exécution de la requête
            $stmt->execute();

            // Renvoyer les séries
            return array('success' => true);
        } catch (PDOException $e) {
            // Gestion des erreurs PDO
            return array('success' => false, 'error' => 'Erreur lors de l\'ajout de l\'utilisateur : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de données
            $conn = null;
        }
    } else {
        return array('success' => false,'error' => 'Erreur de connexion à la base de données.');
    }
}
//Fonction Suppression Utilisateur
function DeleteUser($user_name , $password) {
    // Connexion à la base de données
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Requête pour supprimer un utilisateur
            $query = "DELETE FROM utilisateurs WHERE nom_user = :user_name AND mdp = :password";

            // Préparation de la requête
            $stmt = $conn->prepare($query);

            // Liaison des paramètres
            $stmt->bindParam(':user_name', $user_name);
            $stmt->bindParam(':password', $password);

            // Exécution de la requête
            $stmt->execute();

            // Renvoyer les séries
            return "Utilisateur supprimé";
        } catch (PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la suppression de l\'utilisateur : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de données
            $conn = null;
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de données.');
    }
}
//Fonction Mise à jour Utilisateur
function UpdateUser($user_id, $user_name, $user_email, $user_password) {
    // Connexion à la base de données
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Requête pour mettre à jour un utilisateur
            $query = "UPDATE utilisateurs SET nom_user = :user_name, email = :user_email, mdp = :user_password WHERE id_user = :user_id";

            // Préparation de la requête
            $stmt = $conn->prepare($query);

            // Liaison des paramètres
            $stmt->bindParam(':user_id', $user_id);
            $stmt->bindParam(':user_name', $user_name);
            $stmt->bindParam(':user_email', $user_email);
            $stmt->bindParam(':user_password', $user_password);

            // Exécution de la requête
            $stmt->execute();

            // Renvoyer un message de succès
            return "Utilisateur mis à jour";
        } catch (PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la mise à jour de l\'utilisateur : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de données
            $conn = null;
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de données.');
    }
}
//Fonction Ajout Series Likees
function UpdateLikedSeries($user_name , $password, $liked_series) {
    // Connexion à la base de données
    $conn = connectToDatabase();

    if ($conn) {
        try {
            // Requête pour mettre à jour les séries aimées de l'utilisateur
            $query = "UPDATE utilisateurs
            SET series_likes = IF(FIND_IN_SET(:liked_series, series_likes) > 0, series_likes, CONCAT_WS(',', series_likes, :liked_series))
            WHERE nom_user = :user_id AND mdp = :password";

            // Préparation de la requête
            $stmt = $conn->prepare($query);

            // Liaison des paramètres
            $stmt->bindParam(':user_id', $user_name);
            $stmt->bindParam(':password', $password);
            $stmt->bindParam(':liked_series', $liked_series);

            // Exécution de la requête
            $stmt->execute();

            // Renvoyer un message de succès
            return "Séries aimées mises à jour";
        } catch (PDOException $e) {
            // Gestion des erreurs PDO
            return array('error' => 'Erreur lors de la mise à jour des séries aimées : ' . $e->getMessage());
        } finally {
            // Fermeture de la connexion à la base de données
            $conn = null;
        }
    } else {
        return array('error' => 'Erreur de connexion à la base de données.');
    }
}

// Code pour traiter la requête

// Vérifier la méthode de la requête
$method = $_SERVER['REQUEST_METHOD'];

switch($method){
    case 'GET' :
        $request = $_SERVER['REQUEST_URI'];
        if ($request === '/saes5/test_api3.php/series') {
            echo json_encode(getAllSeriesNames());
        } else {
            // Renvoyer une erreur si la requête n'est pas reconnue
            header('HTTP/1.1 404 Not Found');
            exit();
        }
        break;
    case 'POST' :
        // Récupérer les données de la requête
        $data = json_decode(file_get_contents('php://input'), true);
        $request = $_SERVER['REQUEST_URI'];
        if ($request === '/saes5/test_api3.php/serie/info') {
            // Récupérer les informations de la série
            $seriesInfo = json_encode(getSeriesInfoByName($data['nom_serie'], $data['langue']));
            echo $seriesInfo;
        } elseif ($request === '/saes5/test_api3.php/user/info') {
            // Récupérer les informations de l'utilisateur
            $userInfo = json_encode(getUserInfo($data['user_name'],$data['password']));
            echo $userInfo;
        } elseif ($request === '/saes5/test_api3.php/user/likes') {
            // Récupérer les séries likées de l'utilisateur
            $seriesLikes = json_encode(removeSpecialCharacters(getSeriesLikes($data['user_name'],$data['password'])));
            echo $seriesLikes;
        } elseif ($request === '/saes5/test_api3.php/user/recos') {
            // Récupérer les séries recommandées de l'utilisateur
            $seriesRecommandees = sortByOccurrence(splitStringsIntoWords(removeSpecialCharacters(getRecos($data['user_name'],$data['password'], $data['langue']))));
            $seriesLikes = removeSpecialCharacters(getSeriesLikes($data['user_name'],$data['password']));
            $seriesRecosFiltres = removeElementsFromList($seriesLikes, $seriesRecommandees);
            $seriesRecosFiltres = array_values($seriesRecosFiltres);
            echo json_encode($seriesRecosFiltres);
        } elseif ($request === '/saes5/test_api3.php/series/genre') {
            // Récupérer les séries d'un genre donné
            $series = json_encode(getGenres($data['genre'], $data['langue']));
            echo $series;
        } elseif ($request === '/saes5/test_api3.php/series/search') {
            // Recherche d'une serie par nom
            $series = json_encode(sortByOccurrence(searchSeriesByName($data['nom_serie'])));
            echo $series;
        } elseif ($request === '/saes5/test_api3.php/series/search/phrase') {
            // Recherche TF_IDF
            $series = searchByPhrase($data['phrase'], $data['langue']);
            echo json_encode($series);
        }elseif($request === '/saes5/test_api3.php/user/verify'){
            // Vérifier si un utilisateur existe
            $userExists = userExists($data['nom_user'], $data['password']);
            if ($userExists) {
                http_response_code(200);
            } else {
                http_response_code(400);
                echo json_encode(array('success' => false, 'error' => 'Unknown user'));
            }
        }else{
            // Renvoyer une erreur si la requête n'est pas reconnue
            header('HTTP/1.1 404 Not Found');
            exit();
        }
        break;
    case 'PUT' :
        // Récupérer les données de la requête
        $data = json_decode(file_get_contents('php://input'), true);
        $request = $_SERVER['REQUEST_URI'];
        // Ajouter un utilisateur
        if ($request === '/saes5/test_api3.php/user/add') {

            error_log('Appel de la fonction AddUser en cours');
            $result = AddUser($data['user_id'], $data['user_name'], $data['user_email'], $data['user_password'], json_encode(null));
            error_log('Appel de la fonction AddUser terminé');
            if ($result['success']==true) {
                http_response_code(200);
            } else {
                http_response_code(400);
                echo json_encode(array('success' => false, 'error' => isset($result['error']) ? $result['error'] : 'Unknown error'));
            }
            echo json_encode($result);
        } elseif ($request === '/saes5/test_api3.php/user/update') {
            // Mettre à jour un utilisateur
            $result = UpdateUser($data['user_id'], $data['user_name'], $data['user_email'], $data['user_password']);
            if ($result['success']==true) {
                http_response_code(200);
            } else {
                http_response_code(400);
                echo json_encode(array('success' => false, 'error' => isset($result['error']) ? $result['error'] : 'Unknown error'));
            }
            echo json_encode($result);
        } elseif ($request === '/saes5/test_api3.php/user/likes/update') {
            // Mettre à jour les séries likées de l'utilisateur
            $result = UpdateLikedSeries($data['user_id'], $data['password'], $data['liked_series']);
            if ($result == "Séries aimées mises à jour") {
                http_response_code(200);
            } else {
                http_response_code(400);
                echo json_encode(array('success' => false, 'error' => isset($result['error']) ? $result['error'] : 'Unknown error'));
            }
            echo json_encode($result);
        } else {
            // Renvoyer une erreur si la requête n'est pas reconnue
            http_response_code(404);
            echo json_encode(array('success' => false, 'error' => 'Unknown request'));
            exit();
        }        

        break;
    case 'DELETE' :
        // Récupérer les données de la requête
        $data = json_decode(file_get_contents('php://input'), true);
        $request = $_SERVER['REQUEST_URI'];
        // Supprimer un utilisateur
        if ($request === '/saes5/test_api3.php/user/delete') {
            echo json_encode(DeleteUser($data['user_name'],$data['password']));
        } else {
            // Renvoyer une erreur si la requête n'est pas reconnue
            header('HTTP/1.1 404 Not Found');
            exit();
        }
        break;
    default :
        echo "Méthode non autorisée";
        break;
}
