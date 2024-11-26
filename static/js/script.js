
// Définir les dimensions de l'image (en coordonnées simples)
var imageBounds = [[0, 0], [1571, 2069]];

// Initialiser la carte Leaflet
var map = L.map('map', {
    crs: L.CRS.Simple,
    minZoom: -2,
    maxZoom: 1,
    attributionControl: false
});

// Ajouter l'image de la carte en superposition
var imageUrl = '/static/images/test2.png';
L.imageOverlay(imageUrl, imageBounds).addTo(map);

// Ajuster la vue de la carte pour qu'elle s'adapte à l'image
map.fitBounds(imageBounds);

// Groupes pour les catégories
var solarCoins = L.layerGroup();
var reputation = L.layerGroup();
var clan = L.layerGroup();
var tresor = L.layerGroup();
var epaves = L.layerGroup();
var epaves2 = L.layerGroup();
// Fonction pour charger et afficher les données du fichier JSON
function loadMarkers(district = "all") {
    // Vider les groupes de couches avant de recharger les marqueurs
    epaves.clearLayers();
    epaves2.clearLayers();
    solarCoins.clearLayers();
    reputation.clearLayers();
    clan.clearLayers();
    tresor.clearLayers();
    // Objet pour stocker les comptes des collectibles par district
    let collectiblesCount = {};
    fetch('/static/data.json')
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
                        case 'reputation':
                            reputation.addLayer(marker);
                            // collectiblesCount[districtKey].solarCoins++;
                            break;
                        case 'clan':
                            clan.addLayer(marker);
                            // collectiblesCount[districtKey].solarCoins++;
                            break;
                        case 'tresor':
                            // collectiblesCount[districtKey].solarCoins++;
                            tresor.addLayer(marker);
                            break;
                        case 'epave':
                            epaves.addLayer(marker);
                            break;
                        case 'epave2':
                            epaves2.addLayer(marker);
                            break;   
                    }
                });
            });

            // Ajouter les couches à la carte
            map.addLayer(solarCoins);
            map.addLayer(reputation);
            map.addLayer(clan);
            map.addLayer(tresor);
            map.addLayer(epaves);
            map.addLayer(epaves2);
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
        case 'reputation': return '/static/images/reputation2.png';
        case 'clan': return '/static/images/clan.png';
        case 'tresor': return '/static/images/tresor.png';
        case 'epave': return '/static/images/epaves.png';
        case 'epave2': return '/static/images/epaves2.png';
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

document.getElementById('toggle-reputation').onclick = function() {
    if (map.hasLayer(reputation)) {
        map.removeLayer(reputation);
    } else {
        map.addLayer(reputation);
    }
};

document.getElementById('toggle-clan').onclick = function() {
    if (map.hasLayer(clan)) {
        map.removeLayer(clan);
    } else {
        map.addLayer(clan);
    }
};

document.getElementById('toggle-tresor').onclick = function() {
    if (map.hasLayer(tresor)) {
        map.removeLayer(tresor);
    } else {
        map.addLayer(tresor);
    }
};

document.getElementById('toggle-epaves').onclick = function() {
    if (map.hasLayer(epaves)) {
        map.removeLayer(epaves);
    } else {
        map.addLayer(epaves);
    }
};

document.getElementById('toggle-epaves2').onclick = function() {
    if (map.hasLayer(epaves2)) {
        map.removeLayer(epaves2);
    } else {
        map.addLayer(epaves2);
    }
};
document.getElementById('toggle-tutoepaves').onclick = function() {
    window.open("https://www.youtube.com/watch?v=OTd32jPfsB8", "_blank");
    
};




document.getElementById('districtvideo-select').addEventListener('change', function() {
    var selectedDistrict = this.value;

    switch(selectedDistrict) {
        case 'district1':
            window.open("https://www.youtube.com/watch?v=qITBPJ3I0oU", "_blank");
            break;
        case 'district2':
            window.open("https://www.youtube.com/watch?v=kLAFxxGVSUQ", "_blank");
            break;
        case 'district3':
            window.open("https://www.youtube.com/watch?v=17yjcAzInNA", "_blank");
            break;
        
        case 'district4':
            window.open("https://www.youtube.com/watch?v=0JnoxfzGP4c", "_blank");
            break;
        
        case 'district5':
            window.open("https://www.youtube.com/watch?v=Kj20xFMnd-8", "_blank");
            break;
        
        case 'district6':
            window.open("https://www.youtube.com/watch?v=QdKhUUNQRNQ", "_blank");
            break;
        case 'district7':
                window.open("https://www.youtube.com/watch?v=YNX4z1S-TSc", "_blank");
            break;
        case 'district8':
                window.open("https://www.youtube.com/watch?v=M2kbOqy22ew", "_blank");
            break;
        case 'district9':
                window.open("https://www.youtube.com/watch?v=WpYW57B3TUk", "_blank");
            break;
        case 'district10':
                window.open("https://www.youtube.com/watch?v=-goiB8z9bf0", "_blank");
            break;
        case 'district11':
                window.open("https://www.youtube.com/watch?v=i7Y9dAtUYQs&t=171s", "_blank");
            break;
        case 'district12':
                window.open("https://www.youtube.com/watch?v=7azIwKZpBAo", "_blank");
            break;
        case 'district13':
                window.open("https://www.youtube.com/watch?v=mBFMChDMPd0", "_blank");
            break;
        case 'district14':
                window.open("https://www.youtube.com/watch?v=rtMg5j3yqfc", "_blank");
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
    if (map.hasLayer(solarCoins) || map.hasLayer(reputation) || map.hasLayer(clan) || map.hasLayer(tresor) || map.hasLayer(epaves)|| map.hasLayer(epaves2)) {
        map.removeLayer(solarCoins);
        map.removeLayer(reputation);
        map.removeLayer(clan);
        map.removeLayer(tresor);
        map.removeLayer(epaves);
        map.removeLayer(epaves2);
    } else {
        map.addLayer(solarCoins);
        map.addLayer(reputation);
        map.addLayer(clan);
        map.addLayer(tresor);
        map.addLayer(epaves);
        map.addLayer(epaves2);
    }
};

// Fonction pour obtenir les coordonnées au clic
map.on('click', function(e) {
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;
    // console.log(`Coordonnées cliquées : (${lat}, ${lng})`);
    
});

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

    reputation.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('reputation'),
            iconSize: newSize
        }));
    });

    clan.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('clan'),
            iconSize: newSize
        }));
    });

    tresor.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('tresor'),
            iconSize: newSize
        }));
    });

    epaves.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('epave'),
            iconSize: newSize
        }));
    });

    epaves2.eachLayer(function(layer) {
        layer.setIcon(L.icon({
            iconUrl: getIconUrl('epave2'),
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

// changement de langue
// const languageSelect = document.getElementById('language-select');
//         const buttons = document.querySelectorAll('.menu-btn');
//         const title = document.getElementById('title');

//         languageSelect.addEventListener('change', (event) => {
//             const language = event.target.value;
//             buttons.forEach(button => {
//                 button.textContent = button.getAttribute(`data-${language}`);
//             });
//             title.textContent = language === 'fr' ? "Maps interactive Test Drive Unlimited Solar Crown" : "Interactive Maps Test Drive Unlimited Solar Crown";
//         });
        