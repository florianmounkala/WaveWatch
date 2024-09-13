// Récupérez le pseudo et le mot de passe de l'utilisateur de LocalStorage
const userPseudo = localStorage.getItem('userPseudo');
const userPassword = localStorage.getItem('userPassword');
console.log(userPseudo);
console.log(userPassword);
// Description: Script JavaScript pour la page d'accueil   
// Code JavaScript pour la recherche et la liste d'images cliquables
// Utilisez l'élément avec l'ID 'series-list' comme 'seriesContainer'
var seriesContainer = document.getElementById('series-list');
const searchBar = document.querySelector('.search-bar input[type="text"]');



// Fonction pour effectuer la requête lorsque la barre de recherche est vide
function fetchSeries() {
    fetch('http://localhost/saes5/test_api3.php/series', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        data.forEach(seriesName => {
            // Créez un nouvel élément 'li'
            const li = document.createElement('li');

            // Créez un nouvel élément 'img' et définissez son attribut 'src' à l'URL de l'image de la série
            const img = document.createElement('img');
            img.src = `http://localhost/saes5/css_saes5/images/${seriesName}.jpg`;
            img.width = 150;  // Définissez la largeur de l'image
            img.height = 200;  // Définissez la hauteur de l'image
        
            // Créez un nouvel élément 'p' et définissez son texte au nom de la série
            const p = document.createElement('p');
            p.textContent = seriesName;

            // Créez un nouvel élément 'button' pour le bouton "like"
            const button = document.createElement('button');
            button.textContent = "";
            // Ajoutez un écouteur d'événements 'click' au bouton
            button.addEventListener('click', () => {
                // Exécutez une requête à votre API lorsque le bouton est cliqué
                data = {
                    'user_id': userPseudo,
                    'password': userPassword,
                    'liked_series': seriesName
                };
                console.log(data);
                fetch(`http://localhost/saes5/test_api3.php/user/likes/update`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    const message = `Serie ${seriesName} ajoutee aux favoris`;
                    console.log(data);
                    console.log(message);
                    alert(message);
                })
                .catch(error => console.error('Erreur :', error));
            });
        
            // Ajoutez l'image et le nom de la série à 'li'
            li.appendChild(img);
            li.appendChild(p);
            li.appendChild(button);

            // Ajoutez 'li' à 'seriesContainer'
            seriesContainer.appendChild(li);
        });
    })
    .catch(error => console.error('Erreur :', error));
}

// Fonction pour effectuer une autre requête lorsque la barre de recherche contient quelque chose
function searchSeries() {
    const searchTerm = searchBar.value;
    langue = "Anglais";
    data = {
        'phrase': searchTerm,
        'langue': langue
    };
    fetch(`http://localhost/saes5/test_api3.php/series/search/phrase`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        // Vérifiez si la réponse est vide
        if (!response.ok || response.status === 204) {
            throw new Error('No content');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        data.forEach(seriesName => {
            // Créez un nouvel élément 'li'
            const li = document.createElement('li');

            // Créez un nouvel élément 'img' et définissez son attribut 'src' à l'URL de l'image de la série
            const img = document.createElement('img');
            img.src = `http://localhost/saes5/css_saes5/images/${seriesName}.jpg`;
            img.width = 150;  // Définissez la largeur de l'image
            img.height = 200;  // Définissez la hauteur de l'image
        
            // Créez un nouvel élément 'p' et définissez son texte au nom de la série
            const p = document.createElement('p');
            p.textContent = seriesName;

            // Créez un nouvel élément 'button' pour le bouton "like"
            const button = document.createElement('button');
            button.textContent = "";
            // Ajoutez un écouteur d'événements 'click' au bouton
            button.addEventListener('click', () => {
                // Exécutez une requête à votre API lorsque le bouton est cliqué
                data = {
                    'user_id': userPseudo,
                    'password': userPassword,
                    'liked_series': seriesName
                };
                console.log(data);
                fetch(`http://localhost/saes5/test_api3.php/user/likes/update`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    const message = `Serie ${seriesName} ajoutee aux favoris`;
                    console.log(data);
                    console.log(message);
                    alert(message);
                })
                .catch(error => console.error('Erreur :', error));
            });
        
            // Ajoutez l'image et le nom de la série à 'li'
            li.appendChild(img);
            li.appendChild(p);
            li.appendChild(button);

            // Ajoutez 'li' à 'seriesContainer'
            seriesContainer.appendChild(li);
        });
    })
    .catch(error => console.error('Erreur :', error));
}

// Fonction pour gérer l'événement de clic sur le bouton de recherche
function handleSearch() {
    // Supprimez toutes les séries de la liste
    seriesContainer.innerHTML = '';
    console.log(seriesContainer);
    // Vérifiez si la barre de recherche est vide
    if (searchBar.value === '') {
        fetchSeries();
    } else {
        searchSeries();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Ajouter un gestionnaire d'événement au bouton de recherche
    document.getElementById('search-button').addEventListener('click', handleSearch);
    // Faire une requête pour obtenir la liste des séries
    fetchSeries();
});
