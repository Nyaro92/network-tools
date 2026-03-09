from flask import Flask,render_template,request
import check
from flask import jsonify

app= Flask(__name__)
@app.route("/")
def principe():
   return render_template("check.html")
@app.route("/ping", methods=['GET', 'POST'])
def ping():
    if request.method == 'GET':
        return render_template('bande.html')
    result = None
    action=request.form.get("action")
    if request.method == "POST":
        host = request.form.get("lien")
        packets = request.form.get("paquets") or 4
        if action == "btn_pingeo":
            print("action reçu: ", action )
            return jsonify(check.ping_os(packets, host))
        
        elif action == "btn_mtr":
            return jsonify(check.mtr_os(host))
        else:
            return jsonify({"erreur : action pas trouvé "})



@app.route("/tester_vitesse", methods=['GET', 'POST'])
def bande_passante():
   # On appelle la fonction et on récupère le dictionnaire
   donnees = check.bande_passante()
   # On le transforme en JSON pour le JavaScript
   return jsonify(donnees)
if __name__== "__main__":
   app.run(debug=True,host="127.0.0.1", port=5000)