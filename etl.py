import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Execute the COPY command for all queries stored in the 'copy_table_queries' list to load data into the staging tables.

    Parameters:
    cur (psycopg2.extensions.cursor): The cursor object. Manages the context of a fetch operation.
    conn (psycopg2.extensions.connection): The connection object. Handles the connection to a PostgreSQL database instance.

    Returns:
    None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Execute the INSERT command for all queries stored in the 'insert_table_queries' list to ingest data from staging into the 
        tables in the Amazon EC2.

    Parameters:
    cur (psycopg2.extensions.cursor): The cursor object. Manages the context of a fetch operation.
    conn (psycopg2.extensions.connection): The connection object. Handles the connection to a PostgreSQL database instance.

    Returns:
    None
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Read configuration file, establish DWH connection and call load and insert functions.
    
    Parameters: 
    None
    
    Returns:
    None
    """

    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()