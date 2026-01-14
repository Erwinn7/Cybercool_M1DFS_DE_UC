// Gestion de la soumission du formulaire
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('fm1');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            
            try {
                const formData = new FormData();
                formData.append('username', username);
                
                const response = await fetch('http://127.0.0.1:8000/login', {
                    method: 'POST',
                    body: formData
                });
                
                // const data = await response.json();
            } catch (error) {
            }
            window.location.href = 'avertissement.html'
        });
    }
});

window.addEventListener('load', function() {
    // Regarder si l'URL contient 'support=QRcode'
    const urlParams = new URLSearchParams(window.location.search);
    let support = 'url'
    if (urlParams.get('support') === 'qrcode') {
        support = 'qrcode';
    }

    if (!sessionStorage.getItem('scanDone')) {
        fetch('http://127.0.0.1:8000/scan', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ support: support })
        })
    }
    sessionStorage.setItem('scanDone', 'true');
});
