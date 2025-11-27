"""
movies_queries.py
Module 7 Assignment
Jordan Dardar
"""

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values


def get_config(env_path: str = ".env") -> dict:
    """Load database connection configuration from a .env file."""
    secrets = dotenv_values(env_path)
    return {
        "user": secrets["USER"],
        "password": secrets["PASSWORD"],
        "host": secrets["HOST"],
        "database": secrets["DATABASE"],
        "raise_on_warnings": True,
    }


try:
    config = get_config()
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\n-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT * FROM studio;")
    studios = cursor.fetchall()
    for studio in studios:
        print(studio)

    print("\n-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT * FROM genre;")
    genres = cursor.fetchall()
    for genre in genres:
        print(genre)

    print("\n-- DISPLAYING Short Film RECORDS (runtime < 2 hours) --")
    cursor.execute("SELECT film_name FROM film WHERE film_runtime < 120;")
    short_films = cursor.fetchall()
    for film in short_films:
        print(film)

    print("\n-- DISPLAYING Director RECORDS in Grouped Order --")
    cursor.execute(
        "SELECT film_director, film_name FROM film ORDER BY film_director;"
    )
    directors = cursor.fetchall()
    for director in directors:
        print(director)

except mysql.connector.Error as err:
    print(err)

finally:
    db.close()
