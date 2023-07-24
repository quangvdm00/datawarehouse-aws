import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Execute the DROP command for all queries stored in the 'drop_table_queries' list to drop all the tables

    Parameters:
    cur (psycopg2.extensions.cursor): The cursor object. Manages the context of a fetch operation.
    conn (psycopg2.extensions.connection): The connection object. Handles the connection to a PostgreSQL database instance.

    Returns:
    None
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Execute the CREATE command for all queries stored in the 'create_table_queries' list to create all the tables

    Parameters:
    cur (psycopg2.extensions.cursor): The cursor object. Manages the context of a fetch operation.
    conn (psycopg2.extensions.connection): The connection object. Handles the connection to a PostgreSQL database instance.

    Returns:
    None
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Read configuration file, establish DWH connection and call drop and create tables functions.
    
    Parameters: 
    None
    
    Returns:
    None
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()