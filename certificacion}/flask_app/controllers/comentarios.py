from flask import abort, redirect, render_template, request, session, url_for
from flask_app import app
from flask_app.models.comentarios import Comentario
from flask_app.models.peliculas import Movie


@app.route("/cine/<int:movie_id>/comentar", methods=["POST"])
def comentar(movie_id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    movie = Movie.get_by_id(movie_id)
    if not movie:
        return redirect(url_for("cine"))

    comentario = request.form.get("content", "").strip()
    if not comentario:
        return redirect(url_for("ver_peli", id=movie_id))

    data = {
        "comentario": comentario,
        "usuario_id": session["user_id"],
        "pelicula_id": movie_id,
    }
    if not Comentario.guardar(data):
        abort(500)
    return redirect(url_for("ver_peli", id=movie_id))


@app.route("/cine/comentario/<int:id>/borrar")
def borrar_comentario(id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    comentario = Comentario.get_by_id(id)
    if not comentario:
        return redirect(request.referrer or url_for("cine"))
    if comentario.usuario_id != session["user_id"]:
        return redirect(request.referrer or url_for("cine"))

    if not Comentario.borrar(id):
        abort(500)
    return redirect(request.referrer or url_for("cine"))



@app.route('/cine/<int:peli_id>')
def ver_pelicula(peli_id):
    # Buscar la película en la base de datos por ID
    pelicula = peliculas_db.get(peli_id)
    
    if not pelicula:
        return "Película no encontrada", 404

    # Enviar los datos a la plantilla HTML
    return render_template('ver_peli.html', pelicula=pelicula)


    