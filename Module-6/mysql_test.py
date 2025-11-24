"""
mysql_test.py
Tests connection to a MySQL database using credentials stored in a `.env` file.

This script assumes that the `.env` file resides in the same directory as
this script and contains the following environment variables without quotes:

USER=root
PASSWORD=your_mysql_password
HOST=localhost
DATABASE=your_database_name

Replace `your_mysql_password` and `your_database_name` with your actual
MySQL password and the name of the database you want to connect to.

Usage:
    python mysql_test.py

Upon successful connection, the script prints out the connection details.
Otherwise, it prints an error message indicating what went wrong.
"""

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values


def get_config(env_path: str = ".env") -> dict:
    """Load database connection configuration from a .env file.

    Args:
        env_path: Relative or absolute path to the .env file.

    Returns:
        A dictionary containing MySQL connection parameters.

    Raises:
        KeyError: If any expected key is missing from the .env file.
    """
    # Load the key-value pairs from the .env file
    secrets = dotenv_values(env_path)

    # Ensure that required keys exist. This will raise a KeyError if
    # any of the expected keys are missing.
    return {
        "user": secrets["USER"],
        "password": secrets["PASSWORD"],
        "host": secrets["HOST"],
        "database": secrets["DATABASE"],
        "raise_on_warnings": True,
    }


def test_connection(config: dict) -> None:
    """Test connection to the MySQL database.

    Attempts to connect to a MySQL database using the provided config.
    If the connection is successful, prints a success message. If not, prints
    an error indicating the failure reason.

    Args:
        config: Dictionary of MySQL connection parameters.
    """
    try:
        # Attempt to connect using the provided configuration
        db = mysql.connector.connect(**config)

        # Output the connection status
        print(
            f"\n Database user '{config['user']}' connected to MySQL on host "
            f"'{config['host']}' with database '{config['database']}'"
        )
        input("\n Press Enter to continue...")

    except mysql.connector.Error as err:
        # Handle specific MySQL errors
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("\n The supplied username or password is invalid.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("\n The specified database does not exist.")
        else:
            print(f"\n Unexpected error: {err}")

    finally:
        # Close the database connection if it exists
        try:
            db.close()
        except Exception:
            pass


if __name__ == "__main__":
    try:
        config_dict = get_config()
    except KeyError as missing_key:
        print(
            f"\n Missing expected key {missing_key!r} in the .env file.\n"
            "Make sure your .env file contains 'USER', 'PASSWORD', 'HOST', and 'DATABASE'."
        )
    else:
        test_connection(config_dict)