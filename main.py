from flask import Flask,render_template,request
import check

app= Flask(__name__)
@app.route("/")
def principe():
   return render_template("check.html")
@app.route("/ping", methods=['GET', 'POST'])
def ping():
   result=None
   host=request.form.get("lien")
   packets=request.form.get("paquets")
   if request.form.get("action") == "btn_pingeo":
      result=check.ping_os(packets, host)
      return render_template("check.html", name= result)
   elif request.form.get("action") == "btn_mtr":
      result=check.mtr_os(host)
      return render_template("check.html", name=result)


@app.route("/connexion", methods=['GET', 'POST'])
def bande_passante():
   lancement=check.bande_passante()
   return render_template("check.html", fct=lancement)

if __name__== "__main__":
   app.run(debug=True,host="127.0.0.1", port=5000)