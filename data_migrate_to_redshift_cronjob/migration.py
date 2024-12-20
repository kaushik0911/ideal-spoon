import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# RDS Configuration
RDS_HOST = os.getenv('DBHOST')
RDS_PORT = os.getenv('DBPORT', 5432)  # Default PostgreSQL port
RDS_USER = os.getenv('DBUSER')
RDS_PASSWORD = os.getenv('DBPASSWORD')
RDS_DB = 'postgres'

# Redshift Configuration
REDSHIFT_HOST = os.getenv('REDSHIFTHOST')
REDSHIFT_PORT = os.getenv('REDSHIFTPORT', 5439)  # Default Redshift port
REDSHIFT_USER = os.getenv('REDSHIFTUSER')
REDSHIFT_PASSWORD = os.getenv('REDSHIFTPASSWORD')
REDSHIFT_DB = os.getenv('REDSHIFTDB')

def fetch_rds_data():
    """Fetch data from the RDS instance."""
    try:
        conn = psycopg2.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB,
            client_encoding='utf8'  # Explicitly set encoding
        )
        query = """
            SELECT
                a.id AS appointment_id,
                d.id AS doctor_id, d.name AS doctor_name, d.specialty,
                p.id AS patient_id, p.name AS patient_name,
                av.date AS appointment_date, av.start_time, av.end_time, a.status AS appointment_status,
                pr.medication, pr.prescribed_date, pr.notes,
                lr.test_name, lr.result AS lab_result, lr.date_conducted
            FROM
                public.records_appointment a
            JOIN public.records_doctor d ON a.doctor_id = d.id
            JOIN public.records_patient p ON a.patient_id = p.id
            JOIN public.records_availability av ON a.availability_id = av.id
            LEFT JOIN public.records_prescription pr ON a.id = pr.appointment_id
            LEFT JOIN public.records_labresult lr ON a.id = lr.appointment_id;
            WHERE
                av.date = CURRENT_DATE - INTERVAL '1 day';
        """
        df = pd.read_sql_query(query, conn)  # Use pd.read_sql_query instead of deprecated pd.read_sql
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching RDS data: {e}")
        raise

def load_to_redshift(dataframe):
    """Load the data into the Redshift instance."""
    try:
        engine = create_engine(
            f'postgresql+psycopg2://{REDSHIFT_USER}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}'
        )
        # Append if table exists; replace otherwise
        dataframe.to_sql('appointment_details', engine, index=False, if_exists='append')
        engine.dispose()
    except Exception as e:
        print(f"Error loading data to Redshift: {e}")
        raise

def run_etl():
    """Run the ETL process."""
    try:
        data = fetch_rds_data()
        print("Data fetched successfully:")
        load_to_redshift(data)
        print("Data loaded successfully to Redshift.")
    except Exception as e:
        print(f"ETL process failed: {e}")

if __name__ == "__main__":
    run_etl()
