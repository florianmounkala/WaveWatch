
// Description: Script JavaScript pour la page d'accueil   
// Code JavaScript pour la recherche et la liste d'images cliquables
// Utilisez l'élément avec l'ID 'series-list' comme 'seriesContainer'
var seriesContainer = document.getElementById('series-list');
const searchBar = document.querySelector('.search-bar input[type="text"]');



// Fonction pour effectuer la requête lorsque la barre de recherche est vide
function fetchSeries(genre) {
    data = {
        'genre': genre ,
        'langue': "Anglais"
    };
    fetch('http://localhost/saes5/test_api3.php/series/genre', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        data = data.filter((seriesName) => seriesName != "");
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
console.log(document.getElementById('genres').value);
fetchSeries(document.getElementById('genres').value);
document.getElementById('genres').addEventListener('change', (event) => {

    // Lorsque l'événement 'change' est déclenché, affichez la valeur sélectionnée
    seriesContainer.innerHTML = "";
    console.log(document.getElementById('genres').value);
    fetchSeries(document.getElementById('genres').value);
});
