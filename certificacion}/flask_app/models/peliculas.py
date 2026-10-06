from flask_app.config.mysqlconnection import connectToMySQL


class Movie:
    db = "certificacion"

    def __init__(self, data):
        self.id = data["id"]
        self.titulo = data["nombre_pelicula"]
        self.director = data["director"]
        self.fecha_estreno = data["fecha_estreno"]
        self.sinopsis = data["sinopsis"]
        self.usuario_id = data["usuario_id"]
        self.creador = data["creador"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = """
            SELECT peliculas.*, usuarios.nombre AS creador
            FROM peliculas
            JOIN usuarios ON peliculas.usuario_id = usuarios.id
            ORDER BY peliculas.created_at DESC;
        """
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return []
        return [cls(movie) for movie in results]

    @classmethod
    def get_by_id(cls, movie_id):
        query = """
            SELECT peliculas.*, usuarios.nombre AS creador
            FROM peliculas
            JOIN usuarios ON peliculas.usuario_id = usuarios.id
            WHERE peliculas.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {"id": movie_id})
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO peliculas
                (nombre_pelicula, director, fecha_estreno, sinopsis, usuario_id, created_at, updated_at)
            VALUES
                (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s, NOW(), NOW());
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
            UPDATE peliculas
            SET nombre_pelicula = %(titulo)s,
                director = %(director)s,
                fecha_estreno = %(fecha_estreno)s,
                sinopsis = %(sinopsis)s,
                updated_at = NOW()
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, movie_id):
        query = "DELETE FROM peliculas WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, {"id": movie_id})

    @staticmethod
    def validate(data):
        return all(
            data.get(field, "").strip()
            for field in ("titulo", "director", "fecha_estreno", "sinopsis")
        )
