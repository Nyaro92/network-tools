/**
 * Anime l'aiguille du compteur
 * @param {string} id - L'ID de l'aiguille (needle-download ou needle-upload)
 * @param {number} value - La valeur en Mbps (0 à 100)
 */
function updateNeedle(id, value) {
    const needle = document.getElementById(id);
    if (!needle) return;

    // On limite entre 0 et 100 pour la sécurité du design
    const safeValue = Math.max(0, Math.min(value, 100));
    
    // Calcul de l'angle : -120deg (0 Mbps) à +120deg (100 Mbps)
    const angle = (safeValue * 2.4) - 120;
    
    // Application de la rotation CSS
    needle.style.transform = `rotate(${angle}deg)`;
}

document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('start-button');
    
    // Log pour confirmer dans la console (F12) que le script est bien lié
    console.log("Système Pingeo prêt. Bouton détecté :", !!startBtn);

    if (startBtn) {
        startBtn.addEventListener('click', function(event) {
            // --- ÉTAPE 1 : BLOQUER LE NAVIGATEUR ---
            // Empêche le navigateur de recharger la page ou d'afficher le JSON brut
            event.preventDefault();
            event.stopPropagation();
            
            const btn = this;
            
            // --- ÉTAPE 2 : ÉTAT DE CHARGEMENT ---
            btn.innerText = "TEST EN COURS...";
            btn.disabled = true;
            btn.style.opacity = "0.7";

            console.log("Requête envoyée au serveur Flask...");

            // --- ÉTAPE 3 : APPEL SERVEUR (FETCH) ---
            fetch('/tester_vitesse', {
                method: 'POST',
                // Pas besoin de headers complexes ici car on n'envoie pas de data, on en reçoit juste
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Le serveur a renvoyé une erreur ' + response.status);
                }
                return response.json(); // Transforme la réponse Flask en objet JS
            })
            .then(data => {
                console.log("Résultats reçus :", data);

                if (data.error) {
                    alert("Erreur Speedtest : Vérifier votre connexion" );
                } else {
                    // --- ÉTAPE 4 : MISE À JOUR VISUELLE ---
                    
                    // On fait bouger les aiguilles
                    updateNeedle('needle-download', data.download);
                    updateNeedle('needle-upload', data.upload);

                    // On affiche les chiffres dans les balises .value
                    const downLabel = document.getElementById('val-download');
                    const upLabel = document.getElementById('val-upload');
                    const result = document.getElementById('resultat');
                    
                    if (downLabel) downLabel.innerText = data.download;
                    if (upLabel) upLabel.innerText = data.upload;
                    if (result) result.innerText = data.observation;
                }
            })
            .catch(error => {
                // Gestion des erreurs réseau (Flask éteint, etc.)
                console.error('Erreur technique :', error);
                alert("Impossible de joindre le serveur. Vérifie que Flask tourne bien.");
            })
            .finally(() => {
                // --- ÉTAPE 5 : RÉINITIALISATION DU BOUTON ---
                btn.innerText = "START";
                btn.disabled = false;
                btn.style.opacity = "1";
            });
        });
    } else {
        console.error("ERREUR : L'ID 'start-button' est introuvable dans ton HTML.");
    }
});