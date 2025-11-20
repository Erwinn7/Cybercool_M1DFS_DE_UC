// Gestion de la soumission du formulaire
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('fm1');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                const formData = new FormData();
                formData.append('username', username);
                formData.append('password', password);
                
                const response = await fetch('http://127.0.0.1:8000/login', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                console.log('Réponse du serveur:', data);
                
                if (response.ok) {
                    alert('Connexion réussie ! Bienvenue ' + data.username);
                } else {
                    alert('Erreur de connexion');
                }
            } catch (error) {
                console.error('Erreur:', error);
                alert('Impossible de se connecter au serveur');
            }
        });
    }
});

window.addEventListener('load', function() {
    // Vérifier si le scan a déjà été fait pendant cette session
    if (!sessionStorage.getItem('scanDone')) {
        fetch('http://127.0.0.1:8000/scan', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(r => { 
            console.log('scan response', r); 
            return r.json(); 
        })
        .then(data => {
            console.log('Scan comptabilisé:', data);
            sessionStorage.setItem('scanDone', 'true');
        })
        .catch(e => console.error('Erreur scan:', e));
    }
});
