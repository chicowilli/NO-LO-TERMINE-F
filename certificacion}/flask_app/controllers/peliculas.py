from flask import abort, flash, redirect, render_template, request, session, url_for
from flask_app import app
from flask_app.models.peliculas import Movie
from flask_app.models.usuarios import User


@app.route("/cine")
def cine():
    if "user_id" not in session:
        return redirect(url_for("index"))

    user = User.get_by_id(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("index"))

    return render_template("registro.html")


@app.route("/cine/nueva")
def nueva_peli():
    if "user_id" not in session:
        return redirect(url_for("index"))

    return render_template("nuevapeli.html")


@app.route("/cine/crear", methods=["POST"])
def crear_peli():
    if "user_id" not in session:
        return redirect(url_for("index"))

    data = {
        "nombre_pelicula": request.form.get("nombre_pelicula", "").strip(),
        "director": request.form.get("director", "").strip(),
        "fecha_estreno": request.form.get("fecha_estreno", "").strip(),
        "sinopsis": request.form.get("sinopsis", "").strip(),
        "usuario_id": session["user_id"],
    }
    if not Movie.validate(data):
        flash("Completa todos los datos de la película.", "peli")
        return redirect(url_for("nueva_peli"))

    if not Movie.save(data):
        abort(500)
    return redirect(url_for("cine"))


@app.route("/cine/<int:id>")
def ver_peli(id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    movie = Movie.get_by_id(id)
    if not movie:
        return redirect(url_for("cine"))
    return render_template("verpeli.html", pelicula=movie)


@app.route("/cine/editar/<int:id>")
def editar_peli(id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    movie = Movie.get_by_id(id)
    if not movie:
        return redirect(url_for("cine"))
    if movie.usuario_id != session["user_id"]:
        flash("Solo puedes editar las películas que creaste.", "peli")
        return redirect(url_for("cine"))

    return render_template("editarpeli.html", pelicula=movie)


@app.route("/cine/actualizar/<int:id>", methods=["POST"])
def actualizar_peli(id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    movie = Movie.get_by_id(id)
    if not movie or movie.usuario_id != session["user_id"]:
        return redirect(url_for("cine"))

    data = {
        "id": id,
        "titulo": request.form.get("titulo", "").strip(),
        "director": request.form.get("director", "").strip(),
        "fecha_estreno": request.form.get("fecha_estreno", "").strip(),
        "sinopsis": request.form.get("sinopsis", "").strip(),
    }
    if not Movie.validate(data):
        flash("Completa todos los datos de la película.", "peli")
        return redirect(url_for("editar_peli", id=id))

    if not Movie.update(data):
        abort(500)
    return redirect(url_for("cine"))


@app.route("/cine/borrar/<int:id>")
def borrar_peli(id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    movie = Movie.get_by_id(id)
    if not movie or movie.usuario_id != session["user_id"]:
        return redirect(url_for("cine"))

    if not Movie.delete(id):
        abort(500)
    return redirect(url_for("cine"))
