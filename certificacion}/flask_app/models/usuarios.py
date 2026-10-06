from flask_app.config.mysqlconnection import connectToMySQL


class User:
    db = "certificacion"

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios
                (nombre, apellido, email, password, created_at, updated_at)
            VALUES
                (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, {"id": user_id})
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def validate_register(cls, data):
        nombre = data.get("nombre", "").strip()
        apellido = data.get("apellido", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        conf_password = data.get("conf_password", "")

        if not nombre or not apellido or not email or not password:
            return False
        if password != conf_password:
            return False
        if cls.get_by_email({"email": email}):
            return False
        return True

    @classmethod
    def validate_login(cls, data):
        user = cls.get_by_email({"email": data.get("email", "").strip()})
        if not user:
            return False, None
        return True, user
