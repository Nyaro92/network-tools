import subprocess 
import platform
import os
import speedtest
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


def ping_os(packets, host):
    #pour le ping , tester le dns et revoir le chemin de nos traffic 
    commande_ping=f"ping -c {packets} {host}"
    commande_dns=f"nslookup {host}"
    commande_traceroute= f" traceroute  {host}"
    
    requete_ping=os.system(commande_ping)
    requete_dns=os.system(commande_dns)
    requete_traceroute= os.system(commande_traceroute)
    print("ito le an'ilay ping_os")
    print(requete_ping)
    print(requete_dns)
    print(requete_traceroute)
#elle combine les 3  le ping + traceroutes + latence 
def mtr_os(host):
    #--report ou -rw pour reporter les analyses
    commande_mtr=f"mtr --report {host}"
    requete_mtr=os.system(commande_mtr)

    print(requete_mtr)


def bande_passante():
    print("bonjour dans notre testeur de connexion!!!!!")
    
    rq=speedtest.Speedtest()
    rq.get_best_server()
    download=rq.download()
    print(download)
 
    upload=rq.upload()
    print(upload)
