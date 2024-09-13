var userPseudo = localStorage.getItem('userPseudo');
var userPassword = localStorage.getItem('userPassword');
// Fonction pour la redirection
function redirect(url) {
    window.location.href = url;
}
// Fonction pour exécuter une requête de type DELETE à votre API
function deleteRequest() {
    data = {
        'user_name': userPseudo,
        'password': userPassword
    };
    console.log(data);
    fetch('http://localhost/saes5/test_api3.php/user/delete', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(function(response) {
        if (response.ok) {
            // Si la réponse est bonne, affichez la réponse dans la console
            console.log(response);
            return response.json();
        }
        throw new Error('Erreur lors de la verification : ' + response.statusText);
    })
    .catch(function(error) {
        // En cas d'erreur réseau, affichez un message d'erreur
        document.getElementById('error-message').style.display = 'block';
        console.error('Erreur lors de bdd :', error.message);
    });

    // Code pour exécuter la requête DELETE à votre API
}

// Écouteur d'événement pour le premier bouton (redirection simple)
document.getElementById('btnRetour').addEventListener('click', function() {
    redirect('http://saes5/page_acceuil_fr.html');
});

// Écouteur d'événement pour le deuxième bouton (redirection + nettoyage du local storage)
document.getElementById('btnDeconnexion').addEventListener('click', function() {
    localStorage.clear();
    redirect('http://saes5/page_connection_fr.html');
});

// Écouteur d'événement pour le troisième bouton (requête DELETE + nettoyage du local storage + redirection)
document.getElementById('btnSupprimer').addEventListener('click', function() {
    deleteRequest();
    alert("Votre compte a été supprimé / Your account has been deleted");
    localStorage.clear();
    redirect('http://saes5/page_connection_fr.html');
});
