import psycopg2
from django.conf import settings
from django.contrib.auth.hashers import make_password


def get_db_connection():
    return psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
    )


def get_db_server_connection():
    return psycopg2.connect(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
    )


def create_database():
    try:
        conn = get_db_server_connection()
        conn.autocommit = True
        cur = conn.cursor()

        db_name = settings.DATABASES['default']['NAME']
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                    (db_name,))
        if cur.fetchone():
            print(f"Database '{db_name}' already exists")
        else:
            # Create the database
            cur.execute(f"CREATE DATABASE {db_name};")
            print(f"Created '{db_name}' database")
            create_tables()

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error while creating DB: {e}")


def create_table(cur, table_name, create_query):
    cur.execute(f"SELECT to_regclass('public.{table_name}')")
    if not cur.fetchone()[0]:
        cur.execute(create_query)
        print(f"Table '{table_name}' created")
    else:
        print(f"Table '{table_name}' already exists")


def create_tables():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # SQL queries for DB tables
        sql_queries = {
            "users": """CREATE TABLE users (
                UserID SERIAL PRIMARY KEY,
                Username VARCHAR(20) NOT NULL,
                Password VARCHAR(100) NOT NULL,
                FullName VARCHAR(70) NOT NULL,
                Role VARCHAR(15) NOT NULL
            );""",

            "contacts": """CREATE TABLE contacts (
                UserID INT NOT NULL,
                PhoneNumber VARCHAR(20) NOT NULL,
                Email VARCHAR(50) NOT NULL,
                PRIMARY KEY (UserID),
                CONSTRAINT fk_contacts_user FOREIGN KEY (UserID)
                REFERENCES "users" (UserID)
            );""",

            "genres": """CREATE TABLE genres (
                GenreID SERIAL PRIMARY KEY,
                Name VARCHAR(35) NOT NULL,
                Description VARCHAR(150) NOT NULL
            );""",

            "engines": """CREATE TABLE engines (
                EngineID SERIAL PRIMARY KEY,
                Name VARCHAR(20) NOT NULL,
                TechFeatures VARCHAR(150) NOT NULL
            );""",

            "programming_languages": """CREATE TABLE programming_languages (
                LanguageID SERIAL PRIMARY KEY,
                Name VARCHAR(20) NOT NULL,
                Description VARCHAR(150) NOT NULL
            );""",

            "applications": """CREATE TABLE applications (
                ApplicationID SERIAL PRIMARY KEY,
                Status VARCHAR(15) NOT NULL,
                task VARCHAR(500) NOT NULL,
                LanguageID INT NOT NULL,
                EngineID INT NOT NULL,
                GenreID INT NOT NULL,
                CONSTRAINT fk_application_language FOREIGN KEY (LanguageID)
                REFERENCES programming_languages (LanguageID),
                CONSTRAINT fk_application_engine FOREIGN KEY (EngineID)
                REFERENCES engines (EngineID),
                CONSTRAINT fk_application_genre FOREIGN KEY (GenreID)
                REFERENCES genres (GenreID)
            );"""
        }

        for table_name, query in sql_queries.items():
            create_table(cur, table_name, query)

        print("Created tables in the database!")

        cur.close()
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error while creating db tables: {e}")


# GET queries
def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    return user


def get_user_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE userid = %s", (id,))
    user = cursor.fetchone()
    return user


# INSERT queries
def create_user(username, password, full_name, role):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = make_password(password)

    cursor.execute("INSERT INTO users (username, password, fullname, role)"
                   "VALUES (%s, %s, %s, %s)",
                   (username, hashed_password, full_name, role))

    conn.commit()
    cursor.close()
    conn.close()
