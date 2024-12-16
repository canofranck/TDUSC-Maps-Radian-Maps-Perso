// Définir les dimensions de l'image (en coordonnées simples)
var imageBounds = [[0, 0], [1440, 1920]];
let showFavorites = true; // État pour savoir si les favoris sont affichés
var friends = []; // Stocker les amis
// Initialiser la carte Leaflet
var map = L.map('map', {
    crs: L.CRS.Simple,
    minZoom: -2,
    maxZoom: 1,
    attributionControl: false
});

var currentIconSize = [25, 25]; // Taille initiale de l'icône

var favoriteIcon = L.icon({
    iconUrl: '/static/images/favori.png',  // Remplace par le chemin de ton icône
    iconSize: currentIconSize,            // Taille de l'icône [largeur, hauteur]
    iconAnchor: [currentIconSize[0] / 2, currentIconSize[1]],          // Point d'ancrage, ici au centre-bas de l'icône
    popupAnchor: [0, -currentIconSize[1]]          // Position du popup par rapport à l'icône
});
var friendIcon = L.icon({
    iconUrl: '/static/images/friend-favorite.png',  // Remplace par le chemin de ton icône
    iconSize: currentIconSize,            // Taille de l'icône [largeur, hauteur]
    iconAnchor: [currentIconSize[0] / 2, currentIconSize[1]],          // Point d'ancrage, ici au centre-bas de l'icône
    popupAnchor: [0, -currentIconSize[1]]          // Position du popup par rapport à l'icône
});

var shop_sharp= L.layerGroup();

var station = L.layerGroup();

var shop_street = L.layerGroup();

// Ajouter l'image de la carte en superposition
var imageUrl = '/static/images/mapsibizaiti.png';
L.imageOverlay(imageUrl, imageBounds).addTo(map);

// Ajuster la vue de la carte pour qu'elle s'adapte à l'image
map.fitBounds(imageBounds);

// Groupes pour les catégories
var favoris = L.layerGroup().addTo(map);

// Fonction pour charger les marqueurs
function loadMarkers2(district = "all") {
    fetch('/favorites_ibiza/')
    .then(response => response.json())
    .then(data => {
        data.forEach(favorite => {
            
            var marker = L.marker([favorite.lat, favorite.lng], { icon: favoriteIcon }).addTo(map)
                .bindPopup(favorite.description);
            marker.on('contextmenu', function () {
                if (confirm(traduction.supfavori)) {
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
    var description = prompt(traduction.entrerfavori);

    if (description) {
        addFavorite_ibiza(lat, lng, description);
    }
});



// Appeler la fonction pour charger les marqueurs
loadMarkers2();
loadMarkers();

// Événement de zoom
map.on('zoomend', updateIconSize);

document.addEventListener('DOMContentLoaded', function() {
    const friendSelect = document.getElementById('friendSelect');
    
    if (friendSelect) {
        friendSelect.addEventListener('change', function() {
            var selectedFriendId = this.value;
            if (selectedFriendId) {
                loadFriendFavorites(selectedFriendId);  // Charger les favoris de l'ami sélectionné
            } else {
                clearFriendMarkers();  // Retirer les favoris si aucun ami n'est sélectionné
            }
        });
    } else {
        console.error('#friendSelect n\'existe pas');
    }
});




// Appelle la fonction pour charger les amis une fois la page chargée
document.addEventListener('DOMContentLoaded', loadFriends);


   




    
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

document.addEventListener('DOMContentLoaded', function() {
    const friendSelect = document.getElementById('friendSelect');
    
    // Vérifie si l'élément #friendSelect existe avant d'ajouter l'événement
    if (friendSelect) {
        friendSelect.addEventListener('change', function() {
            var selectedFriendId = this.value;
            if (selectedFriendId) {
                loadFriendFavorites(selectedFriendId);  // Charger les favoris de l'ami sélectionné
            } else {
                clearFriendMarkers();  // Retirer les favoris si aucun ami n'est sélectionné
            }
        });
    } else {
        console.error('#friendSelect n\'existe pas'); // Log si l'élément n'existe pas
    }
});


// Fonction pour charger les favoris de l'ami sélectionné
function loadFriends() {
    fetch('/get_friends/')
        .then(response => response.json())
        .then(friends => {
            const friendSelect = document.getElementById('friendSelect');
            friendSelect.innerHTML = '';  // Nettoyer d'abord le select
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = traduction.choisirAmi;
            friendSelect.appendChild(defaultOption);

            friends.forEach(friend => {
                const option = document.createElement('option');
                option.value = friend.id;
                option.textContent = friend.username;
                friendSelect.appendChild(option);
            });

            console.log('Amis chargés:', friends);  // Vérifier si les amis sont bien reçus
        })
        .catch(error => console.error('Erreur lors de la récupération des amis:', error));
}

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
    fetch(`/favorites_ibiza/${favoriteId}/delete/`, {
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
// Fonction pour ajouter un favori
function addFavorite_ibiza(lat, lng, description) {
    fetch('ajouter-favori_ibiza/', {
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
    if (currentZoom <= -2) {
        newSize = [25, 25];
    } else if (currentZoom <= -1) {
        newSize = [23, 23];
    } else if (currentZoom >= 0) {
        newSize = [22, 22];
    } else if (currentZoom >= 1) {
        newSize = [23, 23];
    } else {
        newSize = [100, 100];
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
    

    shop_sharp.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('shop_sharp'),
            iconSize: newSize
        }));
    });

    station.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('station'),
            iconSize: newSize
        }));
    });

   
    shop_street.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('shop_street'),
            iconSize: newSize
        }));
    });
   
}
  // Fonction pour ajouter un ami
  function addFriend(userId, friendId) {
      fetch(`/add-friend/${userId}/`, {
          method: 'POST',
          headers: {
              'X-CSRFToken': '{{ csrf_token }}', // Nécessaire pour Django
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              friend_id: friendId  // Envoyer l'ID de l'ami dans le corps de la requête
          })
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              alert(data.message);  // Afficher un message de succès
          } else {
              alert('Erreur : ' + data.message);  // Afficher un message d'erreur
          }
      })
      .catch(error => {
          console.error("Erreur lors de l'ajout de l'ami :", error);
      });
}
  

function loadMarkers(district = "all") {
    // Vider les groupes de couches avant de recharger les marqueurs
     shop_sharp.clearLayers();
     
     station.clearLayers();
     shop_street.clearLayers();
    // Objet pour stocker les comptes des collectibles par district
    let collectiblesCount = {};
    fetch('/static/mymap_ibiza.json')
        .then(response => response.json())
        .then(data => {
            let districtsData = district === "all" ? data.districts : { [district]: data.districts[district] };
            
            // Parcourir les objets dans chaque district
            Object.keys(districtsData).forEach(districtKey => {
                 // Initialiser les compteurs pour ce district
                 collectiblesCount[districtKey] = {
                    solarCoins: 0,
                   
                };
                    districtsData[districtKey].forEach(function(item) {
                    var lat = parseFloat(item.lat);
                    var lng = parseFloat(item.lng);

                    // Définir les icônes avec une taille réduite
                    var icon = L.icon({
                        iconUrl: getIconUrl(item.type),
                        iconSize: [18, 18], // Taille de l'icône réduite
                    });

                    // Créer les marqueurs et les ajouter aux groupes correspondants
                    var marker = L.marker([lat, lng], {icon: icon}).bindPopup(`District: ${district}`);

                    switch(item.type) {
                        case 'shop_sharp':
                            shop_sharp.addLayer(marker);
                            break;
                        
                        case 'station':
                            station.addLayer(marker);
                            break;
                        
                        
                        
                        case 'shop_street':
                            shop_street.addLayer(marker);
                            break;
                        
                    }
                });
            });

            // Ajouter les couches à la carte
            map.addLayer(shop_sharp);
            map.addLayer(station);
             
           
            
            map.addLayer(shop_street);
           
             // Afficher le compte des collectibles par district dans la console
            //console.log("Comptage des collectibles par district :", collectiblesCount);
             // Appeler la fonction pour ajuster les icônes après le chargement des marqueurs
             updateIconSize();
        })
        
        .catch(error => {
            console.error("Erreur lors du chargement du fichier JSON :", error);
        });
}

function getIconUrl(type) {
    switch(type) {
        case 'shop_sharp': return '/static/images/shop_sharp.png';
       
        case 'station': return '/static/images/station.png';
        
        case 'sharp': return '/static/images/sharp.png';
        
        case 'shop_street': return '/static/images/shop_street.png';
        
        default: return '/static/images/default.png';
    }
}
// Fonction pour obtenir les coordonnées au clic
// map.on('click', function(e) {
//     var lat = e.latlng.lat;
//     var lng = e.latlng.lng;
//     console.log(`Coordonnées cliquées : (${lat}, ${lng})`);
    
// });

// Bouton pour tout afficher ou tout cacher
document.getElementById('toggle-all').onclick = function() {
    if (map.hasLayer(shop_sharp) || map.hasLayer(station) ) {
        map.removeLayer(shop_sharp);
        map.removeLayer(station);
        map.removeLayer(shop_street);
        
        
      
        map.removeLayer(shop_street);
     
        } else {
        map.addLayer(shop_sharp);
        map.addLayer(station);
        
        map.addLayer(shop_street);
        
           }
};
document.getElementById('toggleshop_sharp').onclick = function () {
    if (map.hasLayer(shop_sharp)) {
        map.removeLayer(shop_sharp);
    } else {
        map.addLayer(shop_sharp);
    }
};
document.getElementById('togglestation').onclick = function () {
    if (map.hasLayer(station)) {
        map.removeLayer(station);
    } else {
        map.addLayer(station);
    }
};

document.getElementById('togglesshop_street').onclick = function () {
    if (map.hasLayer(shop_street)) {
        
        map.removeLayer(shop_street);
    } else {
        map.addLayer(shop_street);
        
    }
};

