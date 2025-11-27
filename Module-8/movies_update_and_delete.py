"""
Module 8.2 - Movies: Updates & Deletes
Student: Jordan Dardar
File: movies_update_and_delete.py
"""

import mysql.connector
from mysql.connector import errorcode

# ---------- CONNECTION SETUP ----------
# Use the SAME connection info you used in the previous module.
# If your user / password / database are different, change them here.
config = {
    "user": "movies_user",        # <-- change if needed
    "password": "popcorn",        # <-- change if needed
    "host": "127.0.0.1",
    "database": "movies",
    "raise_on_warnings": True
}


# ---------- HELPER FUNCTION TO SHOW FILMS ----------
def show_films(cursor, title):
    """
    Runs an INNER JOIN on film, genre, and studio,
    then prints film name, director, genre, and studio.
    """

    # inner join query (all on one line even if it wraps visually)
    cursor.execute(
        "SELECT film_name AS Name, film_director AS Director, "
        "genre_name AS Genre, studio_name AS 'Studio Name' "
        "FROM film "
        "INNER JOIN genre ON film.genre_id = genre.genre_id "
        "INNER JOIN studio ON film.studio_id = studio.studio_id"
    )

    films = cursor.fetchall()

    print("\n -- {} --".format(title))

    # print each film on its own block
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name: {}\nStudio Name: {}\n"
              .format(film[0], film[1], film[2], film[3]))


# ---------- MAIN PROGRAM ----------
def main():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        # 1) Show the films BEFORE any changes
        show_films(cursor, "DISPLAYING FILMS")

        # 2) INSERT a new film into the film table (NOT 'Star Wars')
        #    Make sure the studio_id and genre_id already exist
        insert_film = (
            "INSERT INTO film (film_name, film_releaseDate, "
            "film_runtime, film_director, studio_id, genre_id) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )

        # Example new movie (you can change the title if you want)
        new_film_data = (
            "Inception",      # film_name
            2010,             # film_releaseDate (year only in this schema)
            148,              # film_runtime (minutes)
            "Christopher Nolan",  # film_director
            1,                # studio_id  (must match an existing studio)
            1                 # genre_id   (must match an existing genre)
        )

        cursor.execute(insert_film, new_film_data)
        db.commit()

        # 3) Show films AFTER INSERT
        show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

        # 4) UPDATE Alien to be a Horror film
        #    This finds the genre_id for 'Horror' and sets Alien to that id.
        update_alien = (
            "UPDATE film "
            "SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror') "
            "WHERE film_name = 'Alien'"
        )

        cursor.execute(update_alien)
        db.commit()

        # 5) Show films AFTER UPDATE
        show_films(cursor, "DISPLAYING FILMS AFTER UPDATE (Alien now Horror)")

        # 6) DELETE the movie Gladiator
        delete_gladiator = "DELETE FROM film WHERE film_name = 'Gladiator'"

        cursor.execute(delete_gladiator)
        db.commit()

        # 7) Show films AFTER DELETE
        show_films(cursor, "DISPLAYING FILMS AFTER DELETE (Gladiator removed)")

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        # basic error handling so the program doesn't just crash silently
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)


if __name__ == "__main__":
    main()
