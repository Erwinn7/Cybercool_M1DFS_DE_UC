/**
 * script.js - Interactions pour la page de sensibilisation cybersécurité
 * Gestion des vidéos cliquables
 */

console.log("Page de sensibilisation cybersécurité - Chargement réussi");

// Attendre que le DOM soit complètement chargé
document.addEventListener('DOMContentLoaded', function() {
    
    // ===== VIDÉOS CLIQUABLES =====
    const videoPreviews = document.querySelectorAll('.video-preview');
    
    videoPreviews.forEach(preview => {
        // Récupérer l'URL de la vidéo depuis l'attribut data
        const videoUrl = preview.getAttribute('data-video-url');
        
        // Si une URL est définie, rendre la prévisualisation cliquable
        if (videoUrl && videoUrl !== '#') {
            preview.addEventListener('click', function(e) {
                // Empêcher le clic de se propager
                e.preventDefault();
                
                // Ouvrir la vidéo dans un nouvel onglet
                window.open(videoUrl, '_blank', 'noopener,noreferrer');
                
                // Log pour le suivi pédagogique
                console.log(`[Pédagogie] Ouverture de la vidéo: ${videoUrl}`);
            });
            
            // Indiquer que c'est cliquable via le curseur
            preview.style.cursor = 'pointer';
            
            // Ajouter un attribut title pour l'accessibilité
            preview.setAttribute('title', 'Cliquez pour regarder la vidéo');
        } else {
            // Pour le placeholder, indiquer qu'il faut remplacer l'URL
            preview.addEventListener('click', function() {
                console.log('⚠️ Remplacez l\'URL de la vidéo dans l\'attribut data-video-url');
                console.log('📹 Exemple: data-video-url="https://www.youtube.com/watch?v=VOTRE_ID"');
                
                // Effet visuel pour indiquer qu'il faut configurer
                this.style.boxShadow = '0 0 0 3px #f59e0b';
                setTimeout(() => {
                    this.style.boxShadow = '';
                }, 1000);
            });
        }
    });
    
    // ===== EFFETS SUR LES CARTES DE CONSEILS =====
    const tipCards = document.querySelectorAll('.tip-card');
    
    tipCards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
    
    // ===== LIENS VIDÉO EXTERNES =====
    const videoLinks = document.querySelectorAll('.video-external-link');
    
    videoLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const linkText = this.textContent.trim();
            console.log(`[Pédagogie] Ouverture du lien vidéo: ${linkText}`);
        });
    });
    
    // ===== LIEN ANSSI =====
    const ansiiLink = document.querySelector('.official-link');
    
    if (ansiiLink) {
        ansiiLink.addEventListener('click', function() {
            console.log('[Ressource] Ouverture du site officiel de l\'ANSSI');
        });
    }
    
    // ===== CONFIGURATION POUR VOTRE VIDÉO =====
    const videoInstruction = document.querySelector('.video-instruction');
    if (videoInstruction) {
        videoInstruction.addEventListener('click', function() {
            console.log('🔧 POUR AJOUTER VOTRE VIDÉO:');
            console.log('1. Trouvez l\'URL de votre vidéo (ex: https://www.youtube.com/watch?v=ABCD1234)');
            console.log('2. Dans index.html, remplacez "VOTRE_ID_VIDEO" par votre ID');
            console.log('3. Optionnel: Ajoutez une miniature personnalisée');
        });
    }
    
    // ===== DÉTECTION DE LA TAILLE D'ÉCRAN =====
    function logScreenSize() {
        const width = window.innerWidth;
        let deviceType = 'Desktop';
        
        if (width <= 768) deviceType = 'Mobile';
        else if (width <= 1024) deviceType = 'Tablette';
        
        console.log(`📱 Affichage ${deviceType}: ${width}px de large`);
    }
    
    // Log initial
    logScreenSize();
    
    // ===== MESSAGE DE BIENVENUE =====
    setTimeout(() => {
        console.log('🔒 Cette simulation pédagogique vise à développer');
        console.log('   des réflexes de cybersécurité au quotidien.');
        console.log('💡 Aucune donnée n\'est collectée - Exercice purement éducatif.');
    }, 500);
});

// Fonction pour changer l'URL de la vidéo (utilitaire)
function setVideoUrl(videoElementId, newUrl, newThumbnailUrl = null) {
    const videoElement = document.querySelector(`[data-video-url="${videoElementId}"]`);
    if (videoElement) {
        videoElement.setAttribute('data-video-url', newUrl);
        
        // Mettre à jour le lien associé
        const linkElement = videoElement.parentElement.querySelector('.video-external-link');
        if (linkElement) {
            linkElement.href = newUrl;
        }
        
        // Mettre à jour la miniature si fournie
        if (newThumbnailUrl) {
            const thumbnail = videoElement.querySelector('.video-thumbnail img');
            if (thumbnail) {
                thumbnail.src = newThumbnailUrl;
            }
        }
        
        console.log(`✅ URL vidéo mise à jour: ${newUrl}`);
    }
}