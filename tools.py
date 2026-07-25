import pandas as pd
import sqlite3

# Helper function to run SQL quert and return a DataFrame
def df_from_query(table, query, params={}):
    try:
        con = sqlite3.connect(table)
        df = pd.read_sql_query(query, con, params=params)
        return df
    finally:
        con.close()

class DB:
    def __init__(self, name):
        # Set database filename with .db extension
        self._dbname = f"./{name}.db"

    def load_from_dataframe(self, df, table_name):
        # Load a DataFrame into a SQLite table (overwrite if it exists)
        con = None
        try:
            con = sqlite3.connect(self._dbname)
            df.to_sql(table_name, con, if_exists="replace", index=False)
        finally:
            if con is not None:
                con.close()

    def query(self, q, params={}):
        # Run a SELECT query and return results as DataFrame
        return df_from_query(self._dbname, q, params=params)

    def execute(self, q):
        # Run a non SELECT query (CREATE/DELETE)
        con = None
        try:
            con = sqlite3.connect(self._dbname)
            cur = con.cursor()
            cur.execute(q)
            con.commit()
        finally:
            if con is not None:
                con.close()
