
// Définir les dimensions de l'image (en coordonnées simples)
var imageBounds = [[0, 0], [1440, 1920]];

// Initialiser la carte Leaflet
var map = L.map('map', {
    crs: L.CRS.Simple,
    minZoom: -1,
    maxZoom: 1,
    attributionControl: false
});

// Ajouter l'image de la carte en superposition
var imageUrl = '/static/images/ibizamaps.png';
L.imageOverlay(imageUrl, imageBounds).addTo(map);

// Ajuster la vue de la carte pour qu'elle s'adapte à l'image
map.fitBounds(imageBounds);

// Groupes pour les catégories
var solarCoins = L.layerGroup();
var reputation = L.layerGroup();
var clan = L.layerGroup();

// Fonction pour charger et afficher les données du fichier JSON
function loadMarkers(district = "all") {
    // Vider les groupes de couches avant de recharger les marqueurs
   
    solarCoins.clearLayers();
   
    clan.clearLayers();
    
    // Objet pour stocker les comptes des collectibles par district
    let collectiblesCount = {};
    fetch('/static/ibiza.json')
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
                        case 'solarCoins':
                            solarCoins.addLayer(marker);
                            // collectiblesCount[districtKey].solarCoins++;
                            break;
                        
                        case 'clan':
                            clan.addLayer(marker);
                            // collectiblesCount[districtKey].solarCoins++;
                            break;
                        
                            
                    }
                });
            });

            // Ajouter les couches à la carte
            map.addLayer(solarCoins);
            
            map.addLayer(clan);
           
          
            
             // Afficher le compte des collectibles par district dans la console
            //console.log("Comptage des collectibles par district :", collectiblesCount);
             // Appeler la fonction pour ajuster les icônes après le chargement des marqueurs
             updateIconSize();
        })
        
        .catch(error => {
            console.error("Erreur lors du chargement du fichier JSON :", error);
        });
}


// Fonction pour obtenir l'URL de l'icône en fonction du type
function getIconUrl(type) {
    switch(type) {
        case 'solarCoins': return '/static/images/SolarCoins.png';
        
        case 'clan': return '/static/images/clan.png';
        
        
        default: return '/static/images/default.png';
    }
}

// Appeler la fonction pour charger les marqueurs
loadMarkers();

// Gestion des événements pour afficher/cacher les couches
document.getElementById('toggle-solarCoins').onclick = function() {
    if (map.hasLayer(solarCoins)) {
        map.removeLayer(solarCoins);
    } else {
        map.addLayer(solarCoins);
    }
};



document.getElementById('toggle-clan').onclick = function() {
    if (map.hasLayer(clan)) {
        map.removeLayer(clan);
    } else {
        map.addLayer(clan);
    }
};




// document.getElementById('toggle-tutoepaves').onclick = function() {
//     window.open("https://www.youtube.com/watch?v=OTd32jPfsB8", "_blank");
    
// };




document.getElementById('districtvideo-select').addEventListener('change', function() {
    var selectedDistrict = this.value;

    switch(selectedDistrict) {
        case 'district1':
            window.open("", "_blank");
            break;
        case 'district2':
            window.open("", "_blank");
            break;
        case 'district3':
            window.open("", "_blank");
            break;
        
        case 'district4':
            window.open("", "_blank");
            break;
        
        case 'district5':
            window.open("", "_blank");
            break;
        
        case 'district6':
            window.open("", "_blank");
            break;
        
        
        default:
             console.log("Aucun district sélectionné");
    }
});


// Gestion de l'événement de changement de district via le menu déroulant
document.getElementById('district-select').addEventListener('change', function() {
    var selectedDistrict = this.value;
    loadMarkers(selectedDistrict);
});
document.getElementById('toggle-flaw').onclick = function() {
    window.open("https://www.youtube.com/@flawmotore", "_blank");
    
};
// Bouton pour tout afficher ou tout cacher
document.getElementById('toggle-all').onclick = function() {
    if (map.hasLayer(solarCoins)  || map.hasLayer(clan) ) {
        map.removeLayer(solarCoins);
        
        map.removeLayer(clan);
        
    } else {
        map.addLayer(solarCoins);
       
        map.addLayer(clan);
        
    }
};



// Fonction pour mettre à jour la taille des icônes en fonction du zoom
function updateIconSize() {
    const currentZoom = map.getZoom(); // Obtenir le niveau de zoom actuel
    // console.log("Niveau de zoom actuel :", currentZoom);
    let newSize;

// Définir la taille des icônes en fonction du zoom
if (currentZoom >= 3) {
    newSize = [60, 60]; // Taille maximale
} else if (currentZoom >= 2) {
    newSize = [40, 40]; // Taille intermédiaire grande
} else if (currentZoom >= 1) {
    newSize = [24, 24]; // Taille intermédiaire
} else if (currentZoom >= 0) {
    newSize = [18, 18]; // Taille par défaut
} else if (currentZoom < 0) {
    newSize = [10, 10]; // Taille minimale pour les niveaux de zoom négatifs
}

       
    // Mettre à jour les icônes dans les groupes de couches
    solarCoins.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('solarCoins'),
            iconSize: newSize
        }));
    });

    

    clan.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('clan'),
            iconSize: newSize
        }));
    });

    

    
}

// Appeler la fonction updateIconSize à chaque changement de zoom
map.on('zoomend', updateIconSize);

// Appeler la fonction pour ajuster les icônes dès le chargement initial
updateIconSize();

// Appeler la fonction updateIconSize à chaque changement de zoom
map.on('zoomend', updateIconSize);

// Appeler la fonction pour ajuster les icônes dès le chargement initial
updateIconSize();

// Fonction pour obtenir les coordonnées au clic
// map.on('click', function(e) {
//     var lat = e.latlng.lat;
//     var lng = e.latlng.lng;
//     console.log(`Coordonnées cliquées : (${lat}, ${lng})`);
    
// });
//             title.textContent = language === 'fr' ? "Maps interactive Test Drive Unlimited Solar Crown" : "Interactive Maps Test Drive Unlimited Solar Crown";
//        