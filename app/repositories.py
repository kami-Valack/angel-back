# Repository layer for database access (hexagonal pattern)
import mysql.connector

class UserRepository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_user_by_email(self, email: str):
        self.cursor.execute(f"SELECT id, nome, email, senha FROM users WHERE email = '{email}'")
        return self.cursor.fetchone()

    def get_user_by_id(self, user_id: int):
        self.cursor.execute(f"SELECT id, nome, email, bio, avatar, createdAt, updatedAt FROM users WHERE id = {user_id}")
        return self.cursor.fetchone()

    def create_user(self, name: str, email: str, password: str):
        self.cursor.execute(f"INSERT INTO users (nome, email, senha) VALUES ('{name}', '{email}', '{password}')")
        self.connection.commit()
        return self.cursor.lastrowid

    def email_exists(self, email: str):
        self.cursor.execute(f"SELECT id FROM users WHERE email = '{email}'")
        return self.cursor.fetchone() is not None
