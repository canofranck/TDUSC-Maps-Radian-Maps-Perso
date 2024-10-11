// Définir les dimensions de l'image (en coordonnées simples)
var imageBounds = [[0, 0], [1571, 2069]];
var showFavorites = true; // État pour savoir si les favoris sont affichés
var friends = []; // Stocker les amis
// Initialiser la carte Leaflet
var map = L.map('map', {
    crs: L.CRS.Simple,
    minZoom: -1,
    maxZoom: 4,
    attributionControl: false
});

var currentIconSize = [20, 20]; // Taille initiale de l'icône

var favoriteIcon = L.icon({
    iconUrl: '/static/images/favori.png',  // Remplace par le chemin de ton icône
    iconSize: currentIconSize,            // Taille de l'icône [largeur, hauteur]
    iconAnchor: [currentIconSize[0] / 2, currentIconSize[1]],          // Point d'ancrage, ici au centre-bas de l'icône
    popupAnchor: [0, -currentIconSize[1]]          // Position du popup par rapport à l'icône
});

// Ajouter l'image de la carte en superposition
var imageUrl = '/static/images/Sans titre.png';
L.imageOverlay(imageUrl, imageBounds).addTo(map);

// Ajuster la vue de la carte pour qu'elle s'adapte à l'image
map.fitBounds(imageBounds);

// Groupes pour les catégories
var favoris = L.layerGroup().addTo(map);

// Fonction pour charger les marqueurs
function loadMarkers(district = "all") {
    fetch('/favorites/')
    .then(response => response.json())
    .then(data => {
        data.forEach(favorite => {
            console.log(`Favorite at: ${favorite.lat}, ${favorite.lng}`);
            var marker = L.marker([favorite.lat, favorite.lng], { icon: favoriteIcon }).addTo(map)
                .bindPopup(favorite.description);
            marker.on('contextmenu', function () {
                if (confirm('Voulez-vous vraiment supprimer ce favori ?')) {
                    deleteFavorite(favorite.id, marker);
                }
            });
        });
        updateIconSize();  // Mettre à jour la taille des icônes après chargement des marqueurs
    })
    .catch(error => {
        console.error("Erreur lors du chargement des favoris :", error);
    });
}

// Quand un utilisateur clique sur la carte
map.on('click', function (e) {
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;
    var description = prompt("Entrez une description pour ce point :");

    if (description) {
        addFavorite(lat, lng, description);
    }
});

// Fonction pour ajouter un favori
function addFavorite(lat, lng, description) {
    fetch('ajouter-favori/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ lat: lat, lng: lng, description: description })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Le favori a été ajouté avec succès !');
            L.marker([lat, lng], { icon: favoriteIcon }).addTo(map)
                .bindPopup(description)
                .openPopup();
        } else {
            alert('Une erreur est survenue : ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}

// Fonction pour mettre à jour la taille des icônes en fonction du zoom
function updateIconSize() {
    const currentZoom = map.getZoom(); // Obtenir le niveau de zoom actuel
    console.log("Niveau de zoom actuel :", currentZoom);
    let newSize;

    // Définir la taille des icônes en fonction du zoom
    if (currentZoom >= 3) {
        newSize = [60, 60];
    } else if (currentZoom >= 2) {
        newSize = [40, 40];
    } else if (currentZoom >= 1) {
        newSize = [24, 24];
    } else if (currentZoom >= 0) {
        newSize = [18, 18];
    } else {
        newSize = [10, 10];
    }

    // Si la taille a changé, mettre à jour l'icône
    if (currentIconSize[0] !== newSize[0] || currentIconSize[1] !== newSize[1]) {
        currentIconSize = newSize;
        favoriteIcon = L.icon({
            iconUrl: '/static/images/favori.png',
            iconSize: currentIconSize,
            iconAnchor: [currentIconSize[0] / 2, currentIconSize[1]],
            popupAnchor: [0, -currentIconSize[1]]
        });
    }
}

// Appeler la fonction pour charger les marqueurs
loadMarkers();

// Événement de zoom
map.on('zoomend', updateIconSize);

// Fonction pour obtenir le cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Fonction pour supprimer un favori
function deleteFavorite(favoriteId, marker) {
    fetch(`/favorites/${favoriteId}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Le favori a été supprimé avec succès.');
            map.removeLayer(marker);
        } else {
            alert('Une erreur est survenue : ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
    });
}


    // Fonction pour charger les amis depuis le serveur
    function loadFriends() {
        fetch('/friends/') // Remplacer par votre endpoint pour récupérer les amis
            .then(response => response.json())
            .then(data => {
                friends = data;
                var friendSelect = document.getElementById('friendSelect');
                friends.forEach(friend => {
                    var option = document.createElement('option');
                    option.value = friend.id; // Assurez-vous que l'ID correspond à votre base de données
                    option.textContent = friend.name; // Remplacez par le nom de l'ami
                    friendSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error("Erreur lors du chargement des amis :", error);
            });
    }

    // Charger les amis au démarrage
    loadFriends();

    // Écouter le clic sur le bouton pour afficher/cacher les favoris
    document.getElementById('toggleMarkers').addEventListener('click', function() {
        showFavorites = !showFavorites; // Alterner l'état
        favoris.eachLayer(layer => {
            if (showFavorites) {
                layer.addTo(map); // Ajouter les favoris à la carte
            } else {
                map.removeLayer(layer); // Retirer les favoris de la carte
            }
        });
    });

// Écouter le changement du sélecteur d'amis
document.getElementById('friendSelect').addEventListener('change', function() {
    var selectedFriendId = this.value;
    if (selectedFriendId) {
        loadFriendFavorites(selectedFriendId);  // Charger les favoris de l'ami sélectionné
    } else {
        // Si aucun ami n'est sélectionné, retirer les marqueurs des favoris de l'ami
        clearFriendMarkers();
    }
});

// Fonction pour retirer les marqueurs des amis précédents
function clearFriendMarkers() {
    map.eachLayer(layer => {
        if (layer instanceof L.Marker && layer.options.icon === friendIcon) {
            map.removeLayer(layer);  // Retirer les marqueurs des favoris de l'ami
        }
    });
}

// Fonction pour charger les favoris de l'ami sélectionné
function loadFriendFavorites(friendId) {
    fetch(`/friends/${friendId}/favorites/`)  // Endpoint pour récupérer les favoris de l'ami
        .then(response => response.json())
        .then(data => {
            clearFriendMarkers();  // Retirer les anciens favoris de l'ami
            data.forEach(favorite => {
                var friendIcon = L.icon({
                    iconUrl: '/static/images/friend-favorite.png',  // Icône pour les favoris de l'ami
                    iconSize: [20, 20],
                    iconAnchor: [10, 20],
                    popupAnchor: [0, -20]
                });
                L.marker([favorite.lat, favorite.lng], { icon: friendIcon })  // Ajouter les nouveaux favoris
                    .addTo(map)
                    .bindPopup(favorite.description);
            });
        })
        .catch(error => {
            console.error("Erreur lors du chargement des favoris de l'ami :", error);
        });
}




