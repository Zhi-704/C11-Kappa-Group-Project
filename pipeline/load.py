"""Script for loading the transformed plant data to the Microsoft SQL Server Database"""

from os import environ as ENV
from dotenv import load_dotenv
from pymssql import connect, Connection, exceptions
from extract import get_all_plant_data
from transform import transform_data


def get_connection() -> Connection:
    """Creates a connection to the database, returning a connection object."""

    try:
        return connect(
            server=ENV["DB_HOST"],
            port=ENV["DB_PORT"],
            user=ENV["DB_USER"],
            password=ENV["DB_PASSWORD"],
            database=ENV["DB_NAME"],
            as_dict=True,
        )
    except KeyError as e:
        raise KeyError(f"{e} missing from environment variables.") from e
    except exceptions.OperationalError as e:
        raise exceptions.OperationalError(
            f"Error connecting to database: {e}") from e


def remove_email_from_dict(reading_dict: dict) -> dict:
    """Removes the email key-value pair from a dictionary,
        returning the new dictionary."""
    return reading_dict.pop("email")


def dictionary_to_tuple(reading_dicts: list[dict]) -> list[tuple]:
    """Converts the transformed plant reading data from a list of dictionaries
        to a list of tuples, returning the list."""

    return [tuple(reading.values()) for reading in reading_dicts]


def retrieve_botanist_ids_and_remove_botanist_emails(reading_dicts: list[dict], connection: Connection) -> list[dict]:
    """Queries the database and retrieves the corresponding botanist ID for each reading
        via their associated email in the reading dict, adding it to each plant reading data dictionary
        and removing the email."""

    for reading in reading_dicts:
        email = reading["email"]

        with connection.cursor() as cursor:

            query = "SELECT botanist_id FROM delta.botanist WHERE email = %s"
            cursor.execute(query, email)

            result = cursor.fetchone()

        reading["botanist_id"] = result["botanist_id"]
        reading = remove_email_from_dict(reading)

    return reading_dicts


def insert_readings(reading_tuples: list[tuple], connection: Connection) -> None:
    """Batch-inserts the plant reading data into the Microsoft SQL Server Database."""

    with connection.cursor() as cursor:

        statement = """
                    INSERT INTO delta.reading(soil_moisture, temperature, timestamp, plant_id, last_watered, botanist_id)
                    VALUES
                        (%s, %s, %s, %s, %s, %s)
                    """
        cursor.executemany(statement, reading_tuples)

    connection.commit()


if __name__ == "__main__":

    load_dotenv()

    reading_data = transform_data(get_all_plant_data())

    connection = get_connection()
    reading_data = retrieve_botanist_ids_and_remove_botanist_emails(
        reading_data, connection)

    reading_data = dictionary_to_tuple(reading_data)

    insert_readings(reading_data, connection)

    connection.close()
