document.addEventListener('DOMContentLoaded', function() {
    const btn_ping = document.getElementById('ping');
    const btn_mtr = document.getElementById('mtr'); // On récupère aussi le bouton MTR
    const result_ping = document.getElementById('req_ping');

    function sendRequest(actionValue) {
        const host = document.getElementById('lien').value;
        const packets = document.getElementById('nombre').value || 4;

        if (!host) {
            alert("Veuillez entrer une adresse !");
            return;
        }

        result_ping.innerText = "Veuillez patienter...";

        const formData = new FormData();
        formData.append('lien', host);
        formData.append('paquets', packets);
        formData.append('action', actionValue); // <--- ON AJOUTE L'ACTION ICI

        fetch('/ping', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error('Erreur serveur: ' + response.status);
            return response.json();
        })
        .then(data => {
            if (!data) {
                result_ping.innerText = "Erreur: Le serveur n'a renvoyé aucune donnée.";
            } else if (data.error) {
                result_ping.innerText = "Erreur : " + data.error;
            } else {
                // On affiche soit requete_ping, soit requete_mtr selon le bouton
                result_ping.innerText = data.requete_ping || data.requete_mtr || "Succès";
            }
        })
        .catch(err => {
            console.error(err);
            result_ping.innerText = "Erreur de connexion au serveur.";
        });
    }

    if (btn_ping) {
        btn_ping.addEventListener('click', (e) => {
            e.preventDefault();
            sendRequest("btn_pingeo");
        });
    }

    if (btn_mtr) {
        btn_mtr.addEventListener('click', (e) => {
            e.preventDefault();
            sendRequest("btn_mtr");
        });
    }
});