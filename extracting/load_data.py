from dotenv import load_dotenv
import psycopg2
from psycopg2 import extras
import os
from os import environ as ENV
from io import StringIO
import boto3
import pandas as pd

def get_s3_client():
    """Create and return S3 client."""
    return boto3.client(
        service_name="s3",
        aws_access_key_id=ENV["AWS_ACCESS_KEY"],
        aws_secret_access_key=ENV["AWS_SECRET_KEY"]
    )

def connect_to_postgres():
    """Return a connection to the RDS database."""
    load_dotenv()
    return psycopg2.connect(dbname=ENV["DB_NAME"],
                            host=ENV["DB_HOST"],
                            user=ENV["DB_USER"],
                            port=ENV["DB_PORT"],
                            password=ENV["DB_PASSWORD"],
                            cursor_factory=psycopg2.extras.RealDictCursor)



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
            print(f'truncating {table}')
            cursor.execute(f'truncate table {table};')
            print(f"Loading {file_path} into {table}...")

            with open(file_path, "r", encoding="utf-8") as f:
                next(f)  # Skip header row
                cursor.copy_from(f, table, sep=",", null="")
            print(f'Data saved to {table}')

        conn.commit()

    conn.close()
    print("All CSVs loaded successfully!")


def download_csv_from_s3_to_dataframe(bucket_name: str, s3_key: str) -> pd.DataFrame:
    """Download CSV from S3 and return as pandas DataFrame."""
    s3_client = get_s3_client()
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        csv_content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_content))
        return df
    except Exception as e:
        print(f"Failed to download {s3_key} from S3: {e}")
        raise


def insert_dataframe_to_postgres(df: pd.DataFrame, table_name: str, conn):
    """Insert DataFrame data into PostgreSQL table."""
    with conn.cursor() as cursor:
        # Truncate table
        print(f'Truncating {table_name}')
        cursor.execute(f'TRUNCATE TABLE {table_name};')
        
        # Convert DataFrame to CSV string for COPY command
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, header=False, na_rep='')
        csv_buffer.seek(0)
        
        # Use COPY to insert data
        print(f"Loading data into {table_name}...")
        cursor.copy_from(csv_buffer, table_name, sep=",", null="")
        print(f'Data saved to {table_name}')


def insert_data_to_db_from_s3():
    """Load data from S3 CSVs into PostgreSQL database."""
    load_dotenv()
    bucket_name = ENV['BUCKET_NAME']
    
    conn = connect_to_postgres()

    # Map S3 CSV keys to table names
    s3_csv_to_tables = {
        "csv_files/ChampionsLeagueStandings.csv": "champions_league_standings",
        "csv_files/PremierLeagueStandings.csv": "premier_league_standings", 
        "csv_files/ChelseaMatches.csv": "chelsea_matches",
        "csv_files/ChelseaPlayers.csv": "chelsea_players",
        "csv_files/CompetitionDetails.csv": "competition_details",
        "csv_files/ChelseaTeamDetails.csv": "chelsea_team_details"
    }

    try:
        for s3_key, table_name in s3_csv_to_tables.items():
            print(f"Processing {s3_key} -> {table_name}")
            
            # Download CSV from S3 as DataFrame
            df = download_csv_from_s3_to_dataframe(bucket_name, s3_key)
            
            # Insert DataFrame into PostgreSQL
            insert_dataframe_to_postgres(df, table_name, conn)

        conn.commit()
        print("All CSVs from S3 loaded successfully into PostgreSQL!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error occurred: {e}")
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    insert_data_to_db()