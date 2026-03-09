import subprocess 
import platform
import os
from urllib.request import build_opener, install_opener
import speedtest
from flask import jsonify
"""
#ping avec subprocess
def ping_subprocess():
    os=platform.system().lower()

    if os=="windows":
        commande=['ping', '-n', '2', '8.8.8.8']

    else:
        commande=['ping', '-c', '2', '8.8.8.8']
    lancement= subprocess.call(commande)
    print("mety le izy fa calme")
    print(lancement)
"""

#on doit utiliser subprocess car os.system donne juste des codes de retour 0 ou 1
def ping_os(packets, host):
    try:
        #pour le ping , tester le dns et revoir le chemin de nos traffic 
        #commande_ping=f"ping -c {packets} {host}"
        commande_ping=['ping', '-c', str(packets), host]
        commande_dns=['nslookup', host]
        commande_traceroute= ['traceroute', host]
        #requete_ping=os.system(commande_ping)
        #on utlise subprocess pour attraper les affichages text , en ajoute decode('utf-8) pour rendre lisibles les octets
        requete_ping=subprocess.check_output(commande_ping,stderr=subprocess.STDOUT).decode('utf-8')
        #requete_dns=os.system(commande_dns)
        requete_dns=subprocess.check_output(commande_dns, stderr=subprocess.STDOUT).decode('utf-8')
        #requete_traceroute= os.system(commande_traceroute)
        requete_traceroute=subprocess.check_output(commande_traceroute, stderr=subprocess.STDOUT).decode('utf-8')
        print(requete_ping)
        print(requete_dns)
        print(requete_traceroute)
    # Réunir tous les résultat 
        final_result=f"----> RÉSULTAT PING\n {requete_ping} \n\n ----> RÉSULTAT DNS\n {requete_dns}\n\n ----> RÉULTAT DE TRACEROUTE\n {requete_traceroute}"
        return {
            'requete_ping':final_result
        }
    except subprocess.CalledProcessError as e:
        erreur = e.output.decode('utf-8')
        if "Name or service not known" in erreur:
            message = "❌ Domaine invalide ou introuvable."
        elif "100% packet loss" in erreur:
            message = "❌ Hôte inaccessible (100% packet loss)."
        elif "Network is unreachable" in erreur:
            message = "❌ Réseau inaccessible."
        else:
            message = "❌ Erreur lors du ping."

        return {"error": message}

    except Exception as e:
        return {"error": f"Erreur inattendue : {str(e)}"}

#elle combine les 3  le ping + traceroutes + latence 
def mtr_os(host):
    #--report ou -rw pour reporter les analyses
    #commande_mtr=f"mtr --report {host}"
    commande_mtr = ["mtr", "--report", "--report-cycles", "1", host]
    requete_mtr=subprocess.check_output(commande_mtr, stderr=subprocess.STDOUT).decode('utf-8')

    print(requete_mtr)
    return {
        'requete_mtr':requete_mtr
    }
def bande_passante():
    try:
        opener = build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        install_opener(opener)

        st = speedtest.Speedtest(secure=True)
        st.get_best_server()
        
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000

        if download<5:
            observation="CONNEXION : TRÈS LENTE"
        elif 5<=download<10:
            observation="CONNEXION : LENTE"
        elif 10<=download<50:
            observation="CONNEXION : BONNE"
        elif download>=50 :
            observation="CONNEXION : EXCELLENTE"
        # ON ENLEVE LES COMMENTAIRES ICI :
        return {
            'download': round(download, 2),
            'upload' : round(upload, 2),
            'observation':observation
        }
    except Exception as e:
        return {'error': str(e)}

    except subprocess.CalledProcessError as e:
        return {
            "error": "❌ Impossible d'exécuter MTR. Hôte invalide ou inaccessible."
        }