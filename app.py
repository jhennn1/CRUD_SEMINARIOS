from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clavesecreta" 


@app.route("/")
def index():
    inscritos = session.get("inscritos", [])
    return render_template("listado.html", inscritos=inscritos)


@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        fecha = request.form["fecha"]
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        turno = request.form["turno"]

        # Obtener lista de seminarios seleccionados
        seminarios = request.form.getlist("seminarios[]")

        inscritos = session.get("inscritos", [])
        inscritos.append({
            "fecha": fecha,
            "nombre": nombre,
            "apellidos": apellidos,
            "turno": turno,

            # Unir la lista de seminarios en una cadena
            "seminarios": "; ".join(seminarios)
        })
        session["inscritos"] = inscritos
        return redirect(url_for("index"))
    return render_template("registro.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    inscritos = session.get("inscritos", [])
    if id < 0 or id >= len(inscritos):
        return redirect(url_for("index"))

    if request.method == "POST":
        inscritos[id]["fecha"] = request.form["fecha"]
        inscritos[id]["nombre"] = request.form["nombre"]
        inscritos[id]["apellidos"] = request.form["apellidos"]
        inscritos[id]["turno"] = request.form["turno"]
        inscritos[id]["seminarios"] = "; ".join(
            request.form.getlist("seminarios[]"))
        session["inscritos"] = inscritos
        return redirect(url_for("index"))

    inscrito = inscritos[id]


    # Pasar el contacto a la plantilla
    return render_template("editar.html", contacto=inscrito, id=id)


@app.route("/eliminar/<int:id>")
def eliminar(id):
    inscritos = session.get("inscritos", [])
    if id < 0 or id >= len(inscritos):
        return redirect(url_for("index"))
    del inscritos[id]
    session["inscritos"] = inscritos
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)