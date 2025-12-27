import bcrypt
from databases.db import execute_query, fetch_all, fetch_one

class UserRepository:
    @staticmethod
    def add_user(nama, email, plain_password):
        # Hash password sebelum disimpan
        hashed_password = bcrypt.hashpw(
            plain_password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
        
        query = """
            INSERT INTO users (nama, email, password)
            VALUES (?, ?, ?)
        """
        # execute_query harus mengembalikan lastrowid
        return execute_query(query, (nama, email, hashed_password))
    
    @staticmethod
    def verify_user(email, plain_password):
        query = "SELECT id, nama, password FROM users WHERE email = ?"
        user = fetch_one(query, (email,))
        
        if user and bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            user['password'].encode('utf-8')
        ):
            return {
                'id': user['id'],
                'nama': user['nama'],
                'email': email
            }
        return None
        
    @staticmethod
    def verify_password(email, plain_password):
        query = "SELECT password FROM users WHERE email = ?"
        user = fetch_one(query, (email,))
        
        if user and bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            user['password'].encode('utf-8')
        ):
            return True
        return False
    
    @staticmethod
    def update_password_by_email(email, new_plain_password):
        hashed_password = bcrypt.hashpw(
            new_plain_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        query = """
            UPDATE users
            SET password = ?
            WHERE email = ?
        """
        execute_query(query, (hashed_password, email))
    
    @staticmethod
    def get_user_by_id(user_id):
        query = "SELECT * FROM users WHERE id = ?"
        return fetch_one(query, (user_id,))
        
    @staticmethod
    def get_user_by_email(email):
        query = "SELECT id FROM users WHERE email = ?"
        return fetch_one(query, (email,))