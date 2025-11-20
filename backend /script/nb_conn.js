document.addEventListener('DOMContentLoaded', function() {
  // Fonction pour tracker les vues de page
  async function trackPageView() {
    try {
      await fetch('/api/track-pageview', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          page: 'login_page',
          timestamp: new Date().toISOString()
        })
      });
    } catch (error) {
      console.log('Erreur tracking page:', error);
    }
  }

  // Fonction pour tracker les clics
  async function trackLoginClick() {
    try {
      await fetch('/api/track-login-click', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'login_attempt',
          timestamp: new Date().toISOString()
        })
      });
    } catch (error) {
      console.log('Erreur tracking clic:', error);
    }
  }

  // Appel initial pour tracker la vue de page
  trackPageView();

  // Gestion du clic sur le bouton de connexion
  const loginBtn = document.getElementById('login-button');
  if (loginBtn) {
    loginBtn.addEventListener('click', trackLoginClick);
  }
});