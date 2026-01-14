// Gestion de la soumission du formulaire
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('fm1');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // Détecter la source de la visite
            const urlParams = new URLSearchParams(window.location.search);
            const source = urlParams.get('source') || 'direct'; // 'qr' ou 'direct'
            
            try {
                const formData = new FormData();
                formData.append('username', username);
                formData.append('password', password);
                formData.append('source', source);
                
                // Utiliser l'endpoint approprié selon la source
                const endpoint = source === 'qr' ? 'http://127.0.0.1:8000/login/qr' : 'http://127.0.0.1:8000/login/direct';
                
                const response = await fetch(endpoint, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                console.log('Réponse du serveur:', data);
                
                // Toujours afficher le succès (page de test)
                alert('Connexion réussie ! Bienvenue ' + data.username);
            } catch (error) {
                console.error('Erreur:', error);
                alert('Impossible de se connecter au serveur');
            }
        });
    }
});
