import sqlite3
import pandas as pd
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'properties.db')
CSV_FILE = os.path.join(os.path.dirname(__file__), 'properties.csv')

def create_and_populate_db():
    """Creates an SQLite database and populates it with data from properties.csv."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                property_id TEXT PRIMARY KEY,
                location TEXT,
                bhk INTEGER,
                price_lacs REAL,
                amenities TEXT,
                status TEXT,
                contact_person TEXT,
                contact_number TEXT
            )
        ''')
        conn.commit()
        print(f"Table 'properties' ensured in {DB_FILE}")

        # Read data from CSV
        df = pd.read_csv(CSV_FILE)

        # Insert data into the table
        # Using .itertuples() for efficient row iteration
        for row in df.itertuples(index=False):
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO properties (
                        property_id, location, bhk, price_lacs, amenities, status, contact_person, contact_number
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', row)
            except sqlite3.Error as e:
                print(f"Error inserting row {row}: {e}")
        conn.commit()
        print("Data loaded/updated successfully from properties.csv to properties table.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print(f"Error: CSV file not found at {CSV_FILE}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Attempting to create/update database...")
    create_and_populate_db()
    print("Database setup complete.")