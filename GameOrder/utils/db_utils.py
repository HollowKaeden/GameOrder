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
            cur.execute(f"CREATE DATABASE {db_name};")
            print(f"Created '{db_name}' database")

        cur.close()
        conn.close()
        create_tables()
        # Comment this if you don't want example data
        fill_database()

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
            );""",

            "user_application_connect":
            """CREATE TABLE user_application_connect (
                UserID INT NOT NULL,
                ApplicationID int NOT NULL,
                CONSTRAINT fk_user FOREIGN KEY (UserID)
                REFERENCES users (userID),
                CONSTRAINT fk_application FOREIGN KEY (ApplicationID)
                REFERENCES applications (ApplicationID)
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


def fill_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_queries = {
        "programming_languages": """INSERT INTO programming_languages
        (name, description) VALUES
        ('C++', 'Высоко-производительный язык'),
        ('Python', 'Гибкий и удобный для изучения'),
        ('JavaScript', 'Популярный язык для веб-разработки');""",

        "engines": """INSERT INTO engines
        (name, techfeatures) VALUES
        ('Unreal Engine', 'Продвинутая графика, совместимость с VR/AR'),
        ('Unity', 'Кросс-платформенный, поддерживает 2D/3D'),
        ('Godot', 'Открытый код, легкоёмкий');""",

        "genres": """INSERT INTO genres
        (name, description) VALUES
        ('RPG', 'Ролевая игра'),
        ('Platformer', 'Персонаж перемещается между платформами'),
        ('Puzzle', 'Игра с упором на решение загадок');""",

        "applications": """INSERT INTO applications
        (status, task, languageid, engineid, genreid) VALUES
        ('В процессе', 'Создать RPG с открытым миром', '1', '1', '1'),
        ('Выполнено', 'Разработать 2D платформер с авторскими ассетами',
         '2', '2', '2'),
        ('В ожидании', 'Разработать мобильную пазл-игру', '3', '3', '3');""",

        "users": f"""INSERT INTO users
        (username, password, fullname, role) VALUES
        ('admin', '{make_password('admin')}',
         'Артамонов Иван Алексеевич', 'admin'),
        ('Dmitry', '{make_password('passw0rd')}',
         'Петров Дмитрий Владимирович', 'user'),
        ('Olga', '{make_password('1234secure')}',
         'Набокова Ольга Константиновна', 'user');""",

        "contacts": """INSERT INTO contacts VALUES
        ('1', '+1234567890', 'ivan@example.com'),
        ('2', '+0987654321', 'dmitry@example.com'),
        ('3', '+5544332211', 'olga@example.com');""",

        "user_application_connect":
        """INSERT INTO user_application_connect VALUES
        ('1', '1'),
        ('2', '2'),
        ('3', '3');"""
    }

    for table_name, query in sql_queries.items():
        cursor.execute(query)
        print(f'Filled table {table_name} with data!')

    cursor.close()
    conn.commit()
    conn.close()


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


def get_programming_languages():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM programming_languages")
    languages = [{'id': language[0],
                  'name': language[1],
                  'description': language[2]}
                 for language in cursor.fetchall()]
    return languages


def get_engines():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM engines")
    engines = [{'id': engine[0],
                'name': engine[1],
                'description': engine[2]}
               for engine in cursor.fetchall()]
    return engines


def get_genres():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM genres")
    genres = [{'id': genre[0],
               'name': genre[1],
               'description': genre[2]}
              for genre in cursor.fetchall()]
    return genres


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
