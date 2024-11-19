from django.contrib.auth.backends import BaseBackend
from utils.db_utils import get_db_connection


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM users'
                           'WHERE login = %s AND password = %s',
                           (username, password))
            user = cursor.fetchone()

            if user:
                return {
                    'userid': user[0],
                    'login': user[1],
                    'fullname': user[3],
                    'role': user[4]
                }
        except Exception as e:
            print(f'Auth error: {e}')
        finally:
            cursor.close()
            conn.close()

        return None

    def get_user(self, user_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM users WHERE userid = %s',
                           (user_id,))
            user = cursor.fetchone()

            if user:
                return {
                    'userid': user[0],
                    'login': user[1],
                    'fullname': user[3],
                    'role': user[4]
                }
        except Exception as e:
            print(f'User get error: {e}')
        finally:
            cursor.close()
            conn.close()

        return None
