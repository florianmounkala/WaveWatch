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
    data = {
        'user_name': userPseudo,
        'password': userPassword
    };
    fetch('http://localhost/saes5/test_api3.php/user/likes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        data = data.filter((seriesName) => seriesName != 'null');
        console.log(data);
        if (data.length == 0 || data == null){
            alert("Vous n'avez pas liké de séries! Likez des séries pour en avoir !/ You don't yet have enough data to make some favorites. Like series to get them!");
        }
        data.forEach(seriesName => {
            // Créez un nouvel élément 'li'
            const li = document.createElement('li');

            // Créez un nouvel élément 'img' et définissez son attribut 'src' à l'URL de l'image de la série
            const img = document.createElement('img');
            img.src = `http://localhost/saes5/css_saes5/images/${seriesName}.jpg`;
            img.width = 150;  // Définissez la largeur de l'image
            img.height = 200;  // Définissez la hauteur de l'image
            // Ajoutez l'image et le nom de la série à 'li'
            li.appendChild(img);

            // Ajoutez 'li' à 'seriesContainer'
            seriesContainer.appendChild(li);
        });
    })
    .catch(error => console.error('Erreur :', error));
}
fetchSeries();



