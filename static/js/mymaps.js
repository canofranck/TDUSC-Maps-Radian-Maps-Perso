// Définir les dimensions de l'image (en coordonnées simples)
var imageBounds = [[0, 0], [2160,3840]];
var showFavorites = true; // État pour savoir si les favoris sont affichés
var friends = []; // Stocker les amis
// Initialiser la carte Leaflet
var map = L.map('map', {
    crs: L.CRS.Simple,
    minZoom: -2,
    maxZoom: 1,
    attributionControl: false
});

var currentIconSize = [40, 40]; // Taille initiale de l'icône

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
var rassemblement = L.layerGroup();
var atelier = L.layerGroup();
var station = L.layerGroup();
var sharp = L.layerGroup();
var solar = L.layerGroup();
var sharp = L.layerGroup();
var classic = L.layerGroup();
var classic2 = L.layerGroup();
var german = L.layerGroup();
var german2 = L.layerGroup();
var italian = L.layerGroup();
var lamborghini = L.layerGroup();
var luxury = L.layerGroup();
var offroad = L.layerGroup();
var street = L.layerGroup();
var american = L.layerGroup();
var american2 = L.layerGroup();
var asian = L.layerGroup();

var british = L.layerGroup();
var british2 = L.layerGroup();
var ferrari = L.layerGroup();
// Ajouter l'image de la carte en superposition
var imageUrl = '/static/images/CARTE_COMPLETE2.png';
L.imageOverlay(imageUrl, imageBounds).addTo(map);

// Ajuster la vue de la carte pour qu'elle s'adapte à l'image
map.fitBounds(imageBounds);

// Groupes pour les catégories
var favoris = L.layerGroup().addTo(map);

// Fonction pour charger les marqueurs
function loadMarkers2(district = "all") {
    fetch('/favorites/')
    .then(response => response.json())
    .then(data => {
        data.forEach(favorite => {
            
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
            defaultOption.textContent = 'Choisir un ami';
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


function loadFriends() {
    fetch('/get_friends/')
        .then(response => response.json())
        .then(friends => {
            const friendSelect = document.getElementById('friendSelect');
            friendSelect.innerHTML = ''; // Nettoie d'abord le select
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Choisir un ami';
            friendSelect.appendChild(defaultOption);

            friends.forEach(friend => {
                const option = document.createElement('option');
                option.value = friend.id;  // `friend.id` est l'identifiant de l'ami
                option.textContent = friend.username;  // `friend.username` est le nom d'utilisateur de l'ami
                friendSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Erreur lors de la récupération des amis:', error));
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
    solar.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('solar'),
            iconSize: newSize
        }));
    });

    rassemblement.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('rassemblement'),
            iconSize: newSize
        }));
    });

    station.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('station'),
            iconSize: newSize
        }));
    });

    atelier.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('atelier'),
            iconSize: newSize
        }));
    });

    sharp.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('sharp'),
            iconSize: newSize
        }));
    });

    classic.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('classic'),
            iconSize: newSize
        }));
    });
    classic2.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('classic2'),
            iconSize: newSize
        }));
    });
    german.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('german'),
            iconSize: newSize
        }));
    });
    german2.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('german2'),
            iconSize: newSize
        }));
    });
    italian.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('italian'),
            iconSize: newSize
        }));
    });
    lamborghini.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('lamborghini'),
            iconSize: newSize
        }));
    });
    luxury.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('luxury'),
            iconSize: newSize
        }));
    });
    offroad.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('offroad'),
            iconSize: newSize
        }));
    });
    street.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('street'),
            iconSize: newSize
        }));
    });
    american.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('american'),
            iconSize: newSize
        }));
    });
    american2.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('american2'),
            iconSize: newSize
        }));
    });
    asian.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('asian'),
            iconSize: newSize
        }));
    });
    british.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('british'),
            iconSize: newSize
        }));
    });
    british2.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('british2'),
            iconSize: newSize
        }));
    });
    ferrari.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('ferrari'),
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
     rassemblement.clearLayers();
     atelier.clearLayers();
     station.clearLayers();
    
    // Objet pour stocker les comptes des collectibles par district
    let collectiblesCount = {};
    fetch('/static/mymap.json')
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
                        case 'rassemblement':
                            rassemblement.addLayer(marker);
                            break;
                        case 'atelier':
                            atelier.addLayer(marker);
                            break;
                        case 'station':
                            station.addLayer(marker);
                            break;
                        case 'solar':
                            solar.addLayer(marker);
                            break;
                        case 'sharp':
                            sharp.addLayer(marker);
                            break;
                        case 'classic':
                            classic.addLayer(marker);
                            break;
                        case 'classic2':
                            classic2.addLayer(marker);
                            break;
                        case 'german':
                            german.addLayer(marker);
                            break;
                        case 'german2':
                            german2.addLayer(marker);
                            break;
                        case 'italian':
                            italian.addLayer(marker);
                            break;
                        case 'lamborghini':
                            lamborghini.addLayer(marker);
                            break;
                        case 'luxury':
                            luxury.addLayer(marker);
                            break;
                        case 'offroad':
                            offroad.addLayer(marker);
                            break;
                        case 'street':
                            street.addLayer(marker);
                            break;
                        case 'american':
                            american.addLayer(marker);
                            break;
                        case 'american2':
                            american2.addLayer(marker);
                            break;
                        case 'asian':
                            asian.addLayer(marker);
                            break;
                        
                        case 'british':
                            british.addLayer(marker);
                            break;
                        case 'british2':
                            british2.addLayer(marker);
                            break;
                        case 'ferrari':
                            ferrari.addLayer(marker);
                            break;
                    }
                });
            });

            // Ajouter les couches à la carte
            map.addLayer(rassemblement);
            map.addLayer(station);
            map.addLayer(atelier);
            map.addLayer(solar);
            map.addLayer(sharp);
            map.addLayer(classic);
            map.addLayer(classic2);
            map.addLayer(german);
            map.addLayer(german2);
            map.addLayer(italian);
            map.addLayer(lamborghini);
            map.addLayer(luxury);
            map.addLayer(offroad);
            map.addLayer(street);
            map.addLayer(american);
            map.addLayer(american2);
            map.addLayer(asian);
           
            map.addLayer(british);
            map.addLayer(british2);
            map.addLayer(ferrari);
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
        case 'rassemblement': return '/static/images/rassemblement.png';
        case 'atelier': return '/static/images/atelier.png';
        case 'station': return '/static/images/station.png';
        case 'solar': return '/static/images/solar.png';
        case 'sharp': return '/static/images/sharp.png';
        case 'classic': return '/static/images/classic.png';
        case 'classic2': return '/static/images/classic2.png';
        case 'german': return '/static/images/german.png';
        case 'german2': return '/static/images/german2.png';
        case 'italian': return '/static/images/italian.png';
        case 'lamborghini': return '/static/images/lamborghini.png';
        case 'luxury': return '/static/images/luxury.png';
        case 'offroad': return '/static/images/offroad.png';
        case 'street': return '/static/images/street.png';
        case 'american': return '/static/images/american.png';
        case 'american2': return '/static/images/american2.png';
        case 'asian': return '/static/images/asian.png';
        case 'asian2': return '/static/images/asian2.png';
        case 'british': return '/static/images/british.png';
        case 'british2': return '/static/images/british2.png';
        case 'ferrari': return '/static/images/ferrari.png';
        default: return '/static/images/default.png';
    }
}
// Fonction pour obtenir les coordonnées au clic
// map.on('click', function(e) {
//     var lat = e.latlng.lat;
//     var lng = e.latlng.lng;
//     console.log(`Coordonnées cliquées : (${lat}, ${lng})`);
    
// });