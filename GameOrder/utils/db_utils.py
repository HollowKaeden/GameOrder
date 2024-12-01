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
            return False
        else:
            cur.execute(f"CREATE DATABASE {db_name};")
            print(f"Created '{db_name}' database")
            return True
    except Exception as e:
        print(f"Error while creating DB: {e}")
    finally:
        cur.close()
        conn.close()


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
                Password VARCHAR(128) NOT NULL,
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
    except Exception as e:
        print(f"Error while creating db tables: {e}")
    finally:
        cur.close()
        conn.commit()
        conn.close()


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
        ('1', '+1(234)567-89-10', 'ivan@example.com'),
        ('2', '+1(098)765-43-21', 'dmitry@example.com'),
        ('3', '+5(444)333-22-11', 'olga@example.com');""",

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


def initialize_db_features():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_queries = [
        """
        CREATE OR REPLACE FUNCTION AddNewUser(
            user_login VARCHAR(20),
            user_password VARCHAR(128),
            user_fullname VARCHAR(70),
            user_role VARCHAR(15),
            user_phone_number VARCHAR(20),
            user_email VARCHAR(50)
        ) RETURNS VOID AS $$
        DECLARE
            new_user_id INT;
        BEGIN
            INSERT INTO "users" ("username", "password", "fullname", "role")
            VALUES (user_login, user_password, user_fullname, user_role)
            RETURNING "userid" INTO new_user_id;

            INSERT INTO contacts
            VALUES (new_user_id, user_phone_number, user_email);
        END;
        $$ LANGUAGE plpgsql;"""
    ]

    for query in sql_queries:
        cursor.execute(query)
    print('Added procedures, functions and triggers!')

    cursor.close()
    conn.commit()
    conn.close()


def setup_database():
    if create_database():
        create_tables()
        # Comment this if you don't want example data
        fill_database()
        initialize_db_features()


# GET queries
def get_users(filters=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if filters:
        query_filters = list()
        params = list()
        for column, value in filters.items():
            if value and column != 'userid':
                query_filters.append(f'{column} ILIKE %s')
                params.append(f'%{value}%')
        where_clause = ' AND '.join(query_filters) if query_filters else '1=1'
        if filters.get('userid'):
            where_clause += ' AND userid = %s'
            params.append(filters['userid'])
        cursor.execute(f"SELECT * FROM users "
                       f"WHERE {where_clause}", params)
    else:
        cursor.execute("SELECT * FROM users")
    users = [{'id': user[0],
              'username': user[1],
              'password': user[2],
              'fullname': user[3],
              'role': user[4]}
             for user in cursor.fetchall()]

    cursor.close()
    conn.close()

    return users


def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def get_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE userid = %s", (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def get_contacts(filters=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if filters:
        query_filters = list()
        params = list()
        for column, value in filters.items():
            if value and column != 'userid':
                query_filters.append(f'{column} ILIKE %s')
                params.append(f'%{value}%')
        where_clause = ' AND '.join(query_filters) if query_filters else '1=1'
        if filters.get('userid'):
            where_clause += ' AND userid = %s'
            params.append(filters['userid'])
        cursor.execute(f"SELECT * FROM contacts "
                       f"WHERE {where_clause}", params)
    else:
        cursor.execute("SELECT * FROM contacts")
    contacts = [{'id': contact[0],
                 'phonenumber': contact[1],
                 'email': contact[2]}
                for contact in cursor.fetchall()]

    cursor.close()
    conn.close()

    return contacts


def get_contact(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts WHERE userid = %s", (id,))
    contact = cursor.fetchone()

    cursor.close()
    conn.close()

    return contact


def get_programming_languages():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM programming_languages")
    languages = [{'id': language[0],
                  'name': language[1],
                  'description': language[2]}
                 for language in cursor.fetchall()]

    cursor.close()
    conn.close()

    return languages


def get_engines():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM engines")
    engines = [{'id': engine[0],
                'name': engine[1],
                'description': engine[2]}
               for engine in cursor.fetchall()]

    cursor.close()
    conn.close()

    return engines


def get_genres():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM genres")
    genres = [{'id': genre[0],
               'name': genre[1],
               'description': genre[2]}
              for genre in cursor.fetchall()]

    cursor.close()
    conn.close()

    return genres


def get_user_applications(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT app.applicationid,
               app.status,
               app.task,
               lang.name AS language,
               eng.name AS engine,
               genres.name AS genre
        FROM applications AS app
        JOIN user_application_connect AS uac ON
        app.applicationid = uac.applicationid
        JOIN programming_languages AS lang ON app.languageid = lang.languageid
        JOIN engines as eng ON app.engineid = eng.engineid
        JOIN genres ON app.genreid = genres.genreid
        WHERE uac.userid = %s
    """, [user_id])
    applications = [
        {
            'id': row[0],
            'status': row[1],
            'task': row[2],
            'language': row[3],
            'engine': row[4],
            'genre': row[5],
        }
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return applications


def get_application(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications WHERE applicationid = %s",
                   (id,))
    application = cursor.fetchone()

    cursor.close()
    conn.close()
    return application


# INSERT queries
def create_user(username, password, full_name, role, phone_number, email):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = make_password(password)

    cursor.execute("""
        SELECT AddNewUser(%s, %s, %s, %s, %s, %s);
    """, [username, hashed_password, full_name, role, phone_number, email])

    conn.commit()
    cursor.close()
    conn.close()


def create_application(user_id, task, language_id, engine_id, genre_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications (status, task, languageid, engineid, genreid)
        VALUES (%s, %s, %s, %s, %s) RETURNING applicationid;
    """, ['В ожидании', task, language_id, engine_id, genre_id])

    application_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO user_application_connect (userid, applicationid)
        VALUES (%s, %s);
    """, [user_id, application_id])

    conn.commit()
    cursor.close()
    conn.close()


# UPDATE queries
def create_update_lists(db_fields, parameters):
    fields_to_update = list()
    values = list()
    for key, value in parameters.items():
        if key in db_fields and value:
            fields_to_update.append(f"{key} = %s")
            values.append(value)
    return fields_to_update, values


def update_application(pk, parameters):
    conn = get_db_connection()
    cursor = conn.cursor()

    application = get_application(pk)
    if not application:
        return False

    db_fields = ('status', 'task', 'languageid', 'engineid', 'genreid')
    fields_to_update, values = create_update_lists(db_fields, parameters)

    if fields_to_update:
        query = (f"UPDATE applications SET {', '.join(fields_to_update)} "
                 f"WHERE applicationid = %s")
        values.append(pk)
        cursor.execute(query, values)
        conn.commit()

    cursor.close()
    conn.close()

    return True


def update_user(pk, parameters):
    conn = get_db_connection()
    cursor = conn.cursor()

    user = get_user(pk)
    if not user:
        return False

    db_fields = ('username, password, fullname, role')
    fields_to_update, values = create_update_lists(db_fields, parameters)

    if fields_to_update:
        query = (f"UPDATE users SET {', '.join(fields_to_update)} "
                 f"WHERE userid = %s")
        values.append(pk)
        cursor.execute(query, values)
        conn.commit()

    cursor.close()
    conn.close()

    return True


def update_contact(pk, parameters):
    conn = get_db_connection()
    cursor = conn.cursor()

    user = get_contact(pk)
    if not user:
        return False

    db_fields = ('phonenumber', 'email')
    fields_to_update, values = create_update_lists(db_fields, parameters)

    if fields_to_update:
        query = (f"UPDATE contacts SET {', '.join(fields_to_update)} "
                 f"WHERE userid = %s")
        values.append(pk)
        cursor.execute(query, values)
        conn.commit()

    cursor.close()
    conn.close()

    return True


# DELETE queries
def delete_application(pk):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications WHERE applicationid = %s",
                   (pk,))
    application = cursor.fetchone()
    if not application:
        cursor.close()
        conn.close()
        return False

    cursor.execute(("DELETE FROM user_application_connect "
                    "WHERE applicationid = %s"), (pk, ))

    cursor.execute("DELETE FROM applications WHERE applicationid = %s", (pk,))

    conn.commit()
    cursor.close()
    conn.close()
    return True


def delete_user(pk):
    conn = get_db_connection()
    cursor = conn.cursor()

    user = get_user(pk)
    if not user:
        cursor.close()
        conn.close()
        return False

    cursor.execute(("DELETE FROM contacts "
                    "WHERE userid = %s"), (pk, ))

    cursor.execute(("DELETE FROM user_application_connect "
                    "WHERE userid = %s"), (pk, ))

    cursor.execute(("DELETE FROM users "
                    "WHERE userid = %s"), (pk, ))

    conn.commit()
    cursor.close()
    conn.close()
    return True


def delete_contact(pk):
    conn = get_db_connection()
    cursor = conn.cursor()

    contact = get_contact(pk)
    if not contact:
        cursor.close()
        conn.close()
        return False

    cursor.execute(("DELETE FROM contacts "
                    "WHERE userid = %s"), (pk, ))

    cursor.execute(("DELETE FROM user_application_connect "
                    "WHERE userid = %s"), (pk, ))

    cursor.execute(("DELETE FROM users "
                    "WHERE userid = %s"), (pk, ))

    conn.commit()
    cursor.close()
    conn.close()
    return True
