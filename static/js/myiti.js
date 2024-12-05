// Initialisation de la carte Leaflet
var map = L.map('map', {
    crs: L.CRS.Simple,
    minZoom: -2,
    maxZoom: 1,
    attributionControl: false
});

var imageBounds = [[0, 0], [2160,3840]];
L.imageOverlay('/static/images/CARTE_COMPLETE2.png', imageBounds).addTo(map);
map.fitBounds(imageBounds);

let isPlanningRoute = false;
let isSettingArrival = false; // Nouveau booléen pour l'arrivée
let routePoints = {
    depart: null,
    etapes: [],
    arrivee: null
};

// Icônes personnalisées
const startIcon = L.icon({ iconUrl: '/static/images/depart.png', iconSize: [25, 25] });
const waypointIcon = L.icon({ iconUrl: '/static/images/favori.png', iconSize: [20, 20] });
const endIcon = L.icon({ iconUrl: '/static/images/arrive.png', iconSize: [25, 25] });
var currentIconSize = [25, 25]; 
let lignesVisible = false; // Par défaut, les lignes sont visibles
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
// Appelle la fonction pour charger les amis une fois la page chargée
document.addEventListener('DOMContentLoaded', loadFriends);


loadMarkers();
function loadFriends() {
    fetch('/get_friends/')
        .then(response => response.json())
        .then(friends => {
            const friendSelect = document.getElementById('friendSelect');
            friendSelect.innerHTML = ''; // Nettoie d'abord le select
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = traduction.choisirAmi;
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
document.getElementById('friendSelect').addEventListener('change', function () {
    const selectedFriendId = this.value;
    const friendTrajetSelect = document.getElementById('friend-trajets'); // Sélecteur pour les trajets de l'ami
    const userTrajetSelect = document.getElementById('user-trajets'); // Sélecteur pour les trajets de l'utilisateur (si nécessaire)
    
    // Réinitialise uniquement le sélecteur des trajets de l'ami
    friendTrajetSelect.innerHTML = '<option value="">-- Sélectionner un trajet --</option>';
    friendTrajetSelect.disabled = true; // Désactivé par défaut

    if (selectedFriendId) {
        // Charge les trajets de l'ami
        fetch(`/get-friend-trajets/${selectedFriendId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const trajets = data.trajets;
                    if (trajets.length === 0) {
                        alert("Cet ami n'a pas encore de trajets.");
                    } else {
                        trajets.forEach(trajet => {
                            const option = document.createElement('option');
                            option.value = trajet.id;
                            option.textContent = trajet.nom;
                            friendTrajetSelect.appendChild(option);
                        });
                        friendTrajetSelect.disabled = false; // Active le sélecteur si des trajets sont disponibles
                    }
                } else {
                    alert("Erreur lors de la récupération des trajets.");
                }
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des trajets :', error);
                alert("Erreur technique. Veuillez réessayer.");
            });
    }
});

function displayFriendTrajet(trajetId) {
    const friendId = document.getElementById('friendSelect').value; // ID de l'ami sélectionné

    if (friendId && trajetId) {
        fetch(`/get-friend-trajet-details/${trajetId}/?friend_id=${friendId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const trajet = data.trajet;
                    afficherTrajet(trajet); // Appeler la fonction pour afficher sur la carte
                } else {
                    alert("Erreur lors de la récupération des détails du trajet.");
                }
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des détails du trajet :', error);
                alert("Erreur technique. Veuillez réessayer.");
            });
    }
}


// Fonction pour ajouter un marqueur
function addMarker(lat, lng, title) {
    L.marker([lat, lng]).addTo(map).bindPopup(title);
}

// Fonction pour obtenir les limites du trajet
function getBoundsFromTrajet(trajet) {
    // ... (implémentation comme dans la réponse précédente)
}
// Fonction pour afficher les marqueurs sur la carte
let dernierTrajet = null; // Variable globale pour stocker le dernier trajet

function afficherTrajet(trajet) {
    dernierTrajet = trajet; // Enregistre le dernier trajet
    // Efface les lignes et marqueurs existants
    effacerLignes();
    map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    // Afficher le départ
    if (trajet.depart_lat && trajet.depart_lng) {
        L.marker([trajet.depart_lat, trajet.depart_lng], { icon: startIcon })
            .addTo(map)
            .bindPopup("Départ");
    }

    // Afficher les étapes
    if (trajet.etapes) {
        JSON.parse(trajet.etapes).forEach(etape => {
            L.marker([etape.lat, etape.lng], { icon: waypointIcon })
                .addTo(map)
                .bindPopup("Étape");
        });
    }

    // Afficher l'arrivée
    if (trajet.arrivee_lat && trajet.arrivee_lng) {
        L.marker([trajet.arrivee_lat, trajet.arrivee_lng], { icon: endIcon })
            .addTo(map)
            .bindPopup("Arrivée");
    }

    // Tracer la polyligne (uniquement si lignesVisible est true)
    if (lignesVisible) {
        tracerTrajet(trajet);
    }
}

// Écouter le changement du sélecteur de trajets
// Écouteur sur le sélecteur
document.getElementById('trajet').addEventListener('change', function () {
    const selectedTrajetId = this.value;

    if (!selectedTrajetId) {
        alert("Veuillez sélectionner un trajet.");
        return;
    }

    // Requête AJAX pour récupérer les détails du trajet
    fetch(`/afficher_trajets/${selectedTrajetId}/`) // URL dynamique avec l'ID
        .then(response => {
            if (!response.ok) {
                throw new Error("Erreur lors de la récupération des données.");
            }
            return response.json();
        })
        .then(data => {
            afficherTrajet(data); // Appelle la fonction pour afficher les marqueurs
        })
        .catch(error => {
            console.error('Erreur lors du chargement du trajet :', error);
        });
});

// Gestion des événements
document.getElementById("planRoute").addEventListener("click", () => {
    isPlanningRoute = !isPlanningRoute;
    routePoints = { depart: null, etapes: [], arrivee: null };
    document.getElementById("setArrival").disabled = !isPlanningRoute;
    document.getElementById("saveRoute").disabled = !isPlanningRoute;
    alert(isPlanningRoute ? traduction.alertplanningon : traduction.alertplanningoff);
    
});
// Ajouter un point à l'itinéraire
map.on("click", (e) => {
    if (!isPlanningRoute) return;

    if (!routePoints.depart) {
        routePoints.depart = { lat: e.latlng.lat, lng: e.latlng.lng };
        L.marker([e.latlng.lat, e.latlng.lng], { icon: startIcon }).addTo(map).bindPopup("Départ").openPopup();
        alert(traduction.alertpointdepart);
    } else if (isSettingArrival) {
        // Si le mode pour définir l'arrivée est activé
        routePoints.arrivee = { lat: e.latlng.lat, lng: e.latlng.lng };
        L.marker([e.latlng.lat, e.latlng.lng], { icon: endIcon }).addTo(map).bindPopup("Arrivée").openPopup();
        alert(traduction.alertpointarrive);
        isSettingArrival = false; // Désactive le mode arrivée
        document.getElementById("saveRoute").disabled = false; // Active le bouton de sauvegarde
    } else {
        // Sinon, ajouter une étape
        routePoints.etapes.push({ lat: e.latlng.lat, lng: e.latlng.lng });
        L.marker([e.latlng.lat, e.latlng.lng], { icon: waypointIcon }).addTo(map).bindPopup("Étape");
        document.getElementById("setArrival").disabled = false; // Active le bouton d'arrivée
    }
});

document.getElementById("setArrival").addEventListener("click", () => {
    if (routePoints.depart && routePoints.etapes.length > 0) {
        isSettingArrival = true; // Active le mode pour définir l'arrivée
        alert(traduction.messpointarrive);
    } else {
        alert(traduction.errpointarrive);
    }
});

document.getElementById("saveRoute").addEventListener("click", () => {
    const nom = document.getElementById("trajetNom").value;
    if (!nom) {
        alert(traduction.alertnomtraj);
        return;
    }

    const data = {
        nom: nom,
        depart: routePoints.depart,
        etapes: routePoints.etapes,
        arrivee: routePoints.arrivee
    };
    // console.log("Données envoyées :", data); // Vérifier les données avant l'envoi
    fetch('/save_trajet/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(result => {
            // console.log("Résultat de la requête :", result);
            if (result.success) {
                alert(traduction.saveok);
                location.reload();
            } else {
                alert("Erreur : " + result.message);
            }
        })
        .catch(error => console.error("Erreur :", error));
});



// Obtenir le token CSRF
function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        if (cookie.trim().startsWith("csrftoken=")) {
            return cookie.trim().substring("csrftoken=".length);
        }
    }
    return null;
}

function tracerTrajet(trajet) {
    // Préparer les coordonnées pour la polyligne
    const points = [];

    // Ajouter le point de départ
    if (trajet.depart_lat && trajet.depart_lng) {
        points.push([trajet.depart_lat, trajet.depart_lng]);
    }

    // Ajouter les étapes
    if (trajet.etapes) {
        JSON.parse(trajet.etapes).forEach(etape => {
            points.push([etape.lat, etape.lng]);
        });
    }

    // Ajouter le point d'arrivée
    if (trajet.arrivee_lat && trajet.arrivee_lng) {
        points.push([trajet.arrivee_lat, trajet.arrivee_lng]);
    }

    // Tracer la polyligne si au moins deux points existent
    if (points.length >= 2) {
        L.polyline(points, {
            color: 'blue', // Couleur de la ligne
            weight: 4,     // Épaisseur de la ligne
            opacity: 0.7,  // Opacité de la ligne
            smoothFactor: 1
        }).addTo(map);
    }
}
function effacerLignes() {
    if (lignesVisible) {
        // Cacher les lignes
        map.eachLayer(layer => {
            if (layer instanceof L.Polyline) {
                map.removeLayer(layer); // Supprime les polylignes
            }
        });
        lignesVisible = false;
    } else {
        // Réafficher les lignes pour le trajet actuel
        if (dernierTrajet) {
            tracerTrajet(dernierTrajet);
        }
        lignesVisible = true;
    }
}
document.getElementById('toggleLignesBtn').addEventListener('click', function () {
    effacerLignes();

    // Met à jour le texte du bouton
    this.textContent = lignesVisible ? "Cacher les lignes" : "Afficher les lignes";
});

document.getElementById('deleteTrajet').addEventListener('click', function () {
    const trajetSelect = document.getElementById('trajet');
    const trajetId = trajetSelect.value;

    if (!trajetId) {
        alert("Veuillez sélectionner un trajet à supprimer.");
        return;
    }

    // Demander confirmation à l'utilisateur
    if (!confirm("Êtes-vous sûr de vouloir supprimer ce trajet ?")) {
        return;
    }

    // Envoyer une requête POST pour supprimer le trajet
    fetch(`/delete-trajet/${trajetId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value, // CSRF Token
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);

                // Retirer le trajet du sélecteur
                const optionToRemove = trajetSelect.querySelector(`option[value="${trajetId}"]`);
                if (optionToRemove) {
                    optionToRemove.remove();
                }

                // Réinitialiser le sélecteur après suppression
                trajetSelect.value = "";
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Erreur lors de la suppression du trajet :', error);
            alert("Une erreur est survenue. Veuillez réessayer.");
        });
});
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

document.getElementById('toggle-all').onclick = function() {
    if (map.hasLayer(rassemblement) || map.hasLayer(station) || map.hasLayer(atelier) || map.hasLayer(solar) || map.hasLayer(sharp)|| map.hasLayer(classic)) {
        map.removeLayer(rassemblement);
        map.removeLayer(station);
        map.removeLayer(atelier);
        map.removeLayer(solar);
        map.removeLayer(sharp);
        map.removeLayer(classic);
        map.removeLayer(classic2);
        map.removeLayer(german);
        map.removeLayer(german2);
        map.removeLayer(italian);
        map.removeLayer(lamborghini);
        map.removeLayer(luxury);
        map.removeLayer(offroad);
        map.removeLayer(street);
        map.removeLayer(american);
        map.removeLayer(american2);
        map.removeLayer(asian);
       
        map.removeLayer(british);
        map.removeLayer(british2);
        map.removeLayer(ferrari);
        } else {
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
           }
};
document.getElementById('togglerassemblement').onclick = function () {
    if (map.hasLayer(rassemblement)) {
        map.removeLayer(rassemblement);
    } else {
        map.addLayer(rassemblement);
    }
};
document.getElementById('togglestation').onclick = function () {
    if (map.hasLayer(station)) {
        map.removeLayer(station);
    } else {
        map.addLayer(station);
    }
};
document.getElementById('togglesatelier').onclick = function () {
    if (map.hasLayer(atelier)) {
        map.removeLayer(atelier);
    } else {
        map.addLayer(atelier);
    }
};
document.getElementById('togglesconcession').onclick = function () {
    if (map.hasLayer(classic) || map.hasLayer(classic2) ||  map.hasLayer(german)  || map.hasLayer(italian) || map.hasLayer(lamborghini) ) {
        map.removeLayer(classic);
        map.removeLayer(classic2);
        map.removeLayer(german);
        map.removeLayer(german2);
        map.removeLayer(italian);
        map.removeLayer(lamborghini);
        map.removeLayer(luxury);
        map.removeLayer(offroad);
        map.removeLayer(street);
        map.removeLayer(american);
        map.removeLayer(american2);
        map.removeLayer(asian);
        map.removeLayer(british);
        map.removeLayer(british2);
        map.removeLayer(ferrari);
        map.removeLayer(sharp);
                
    } else {
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
        map.addLayer(sharp);
             
    }
};
document.getElementById('togglesclan').onclick = function () {
    if (map.hasLayer(sharp)|| map.hasLayer(street)) {
        map.removeLayer(sharp);
        map.removeLayer(street);
    } else {
        map.addLayer(street);
        map.addLayer(sharp);
    }
};
document.getElementById('togglessolar').onclick = function () {
    if (map.hasLayer(solar)) {
        map.removeLayer(solar);
    } else {
        map.addLayer(solar);
    }
};
