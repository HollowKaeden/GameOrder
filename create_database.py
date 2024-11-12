import psycopg2


def create_database():
    try:
        conn = psycopg2.connect(dbname="PostgreSQL 17", user="postgres",
                                password="postgres", host="localhost")
        conn.autocommit = True
        cur = conn.cursor()

        # Создаем базу данных
        cur.execute("CREATE DATABASE games;")
        print("Database 'games' created successfully")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Ошибка при создании БД: {e}")


def create_tables():
    try:
        conn = psycopg2.connect(dbname="games", user="postgres",
                                password="postgres", host="localhost")
        cur = conn.cursor()

        # Список SQL запросов для создания таблиц
        sql_queries = [
            """CREATE TABLE "user" (
                UserID SERIAL PRIMARY KEY,
                Login VARCHAR(20) NOT NULL,
                Password VARCHAR(50) NOT NULL,
                FullName VARCHAR(70) NOT NULL,
                Role VARCHAR(15) NOT NULL
            );""",

            """CREATE TABLE contacts (
                UserID INT NOT NULL,
                PhoneNumber VARCHAR(20) NOT NULL,
                Email VARCHAR(50) NOT NULL,
                PRIMARY KEY (UserID),
                CONSTRAINT fk_contacts_user FOREIGN KEY (UserID)
                REFERENCES "user" (UserID)
            );""",

            """CREATE TABLE genre (
                GenreID SERIAL PRIMARY KEY,
                Name VARCHAR(35) NOT NULL,
                Description VARCHAR(150) NOT NULL
            );""",

            """CREATE TABLE engine (
                EngineID SERIAL PRIMARY KEY,
                Name VARCHAR(20) NOT NULL,
                TechFeatures VARCHAR(150) NOT NULL
            );""",

            """CREATE TABLE programminglanguage (
                LanguageID SERIAL PRIMARY KEY,
                Name VARCHAR(20) NOT NULL,
                Description VARCHAR(150) NOT NULL
            );""",

            """CREATE TABLE application (
                ApplicationID SERIAL PRIMARY KEY,
                Status VARCHAR(15) NOT NULL,
                task VARCHAR(500) NOT NULL,
                LanguageID INT NOT NULL,
                EngineID INT NOT NULL,
                GenreID INT NOT NULL,
                CONSTRAINT fk_application_language FOREIGN KEY (LanguageID)
                REFERENCES programminglanguage (LanguageID),
                CONSTRAINT fk_application_engine FOREIGN KEY (EngineID)
                REFERENCES engine (EngineID),
                CONSTRAINT fk_application_genre FOREIGN KEY (GenreID)
                REFERENCES genre (GenreID)
            );"""
        ]

        for query in sql_queries:
            cur.execute(query)

        print("Таблицы созданы!")

        cur.close()
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")


def main():
    create_database()
    create_tables()


if __name__ == "__main__":
    main()
