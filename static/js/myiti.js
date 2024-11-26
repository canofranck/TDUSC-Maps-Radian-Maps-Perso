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

let lignesVisible = false; // Par défaut, les lignes sont visibles

// Appelle la fonction pour charger les amis une fois la page chargée
document.addEventListener('DOMContentLoaded', loadFriends);



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
    alert(isPlanningRoute ? "Mode itinéraire activé !" : "Mode itinéraire désactivé.");
    
});
// Ajouter un point à l'itinéraire
map.on("click", (e) => {
    if (!isPlanningRoute) return;

    if (!routePoints.depart) {
        routePoints.depart = { lat: e.latlng.lat, lng: e.latlng.lng };
        L.marker([e.latlng.lat, e.latlng.lng], { icon: startIcon }).addTo(map).bindPopup("Départ").openPopup();
        alert("Point de départ défini !");
    } else if (isSettingArrival) {
        // Si le mode pour définir l'arrivée est activé
        routePoints.arrivee = { lat: e.latlng.lat, lng: e.latlng.lng };
        L.marker([e.latlng.lat, e.latlng.lng], { icon: endIcon }).addTo(map).bindPopup("Arrivée").openPopup();
        alert("Point d'arrivée défini !");
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
        alert("Cliquez sur la carte pour définir l'arrivée.");
    } else {
        alert("Veuillez d'abord définir un point de départ et au moins une étape.");
    }
});

document.getElementById("saveRoute").addEventListener("click", () => {
    const nom = document.getElementById("trajetNom").value;
    if (!nom) {
        alert("Veuillez entrer un nom pour le trajet.");
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
                alert("Trajet sauvegardé avec succès !");
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
