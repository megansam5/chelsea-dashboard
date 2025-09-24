from dotenv import load_dotenv
import psycopg2
from psycopg2 import extras
import os
from os import environ as ENV

def connect_to_postgres():
    """Return a connection to the RDS database."""
    load_dotenv()
    return psycopg2.connect(dbname=ENV["DB_NAME"],
                            host=ENV["DB_HOST"],
                            user=ENV["DB_USER"],
                            port=ENV["DB_PORT"],
                            password=ENV["DB_PASSWORD"],
                            cursor_factory=psycopg2.extras.RealDictCursor)

def create_tables_in_db():
    """Creates the tables in the database"""
    conn = connect_to_postgres()

    with conn.cursor() as cursor:

        # Open and read the schema.sql file
        with open("schema.sql", "r") as f:
            schema_sql = f.read()

        # Execute the SQL commands
        cursor.execute(schema_sql)

        # Commit changes
        conn.commit()

    print("Schema executed successfully!")
    conn.close()

def insert_data_to_db():

    conn = connect_to_postgres()

    # Map CSV filenames to table names
    tables = {
        "ChampionsLeagueStandings.csv": "champions_league_standings",
        "PremierLeagueStandings.csv": "premier_league_standings",
        "ChelseaMatches.csv": "chelsea_matches",
        "ChelseaPlayers.csv": "chelsea_players",
        "CompetitionDetails.csv": "competition_details",
        "ChelseaTeamDetails.csv": "chelsea_team_details"
    }

    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csv_files")
    

    with conn.cursor() as cursor:
        for csv_file, table in tables.items():
            file_path = os.path.join(csv_path, csv_file)
            print(f"Loading {file_path} into {table}...")

            with open(file_path, "r", encoding="utf-8") as f:
                next(f)  # Skip header row
                cursor.copy_from(f, table, sep=",", null="")
            print(f'Data saved to {table}')

        conn.commit()

    conn.close()
    print("All CSVs loaded successfully!")

if __name__ == '__main__':
    insert_data_to_db()