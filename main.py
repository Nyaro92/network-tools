from flask import Flask, render_template, request, jsonify
import check
import os

app = Flask(__name__)

@app.route("/")
def principe():
    return render_template("check.html")

@app.route("/ping", methods=['GET', 'POST'])
def ping():
    if request.method == 'GET':
        return render_template('bande.html')
    action = request.form.get("action")
    host = request.form.get("lien")
    packets = request.form.get("paquets") or 4

    if action == "btn_pingeo":
        return jsonify(check.ping_os(packets, host))
    elif action == "btn_mtr":
        return jsonify(check.mtr_os(host))
    else:
        return jsonify({"erreur": "action pas trouvé"})

@app.route("/tester_vitesse", methods=['GET', 'POST'])
def bande_passante():
    donnees = check.bande_passante()
    return jsonify(donnees)

# Pour tests locaux uniquement
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)