#  Song Play Analysis with S3 and Redshift
## Introduction
In this project, we try to help one music streaming startup, Sparkify, to move their user info and song database processes on to the cloud. Specifically, I build an ETL pipeline that extracts their data from AWS S3 (data storage), stages tables on AWS Redshift (data warehouse with columnar storage), and execute SQL statements that create the analytics tables from these staging tables.

<figure>
  <img src="images/sparkify-s3-to-redshift-etl.png" alt="Sparkify s3 to redshift etl" width=60% height=60%>
</figure>

## Dataset Description
Datasets used in this project are provided in two public S3 buckets. One bucket contains info about songs and artists, the second bucket has info concerning actions done by users (which song are listening, etc.. ). The objects contained in both buckets are **JSON** files.

The Redshift service is where data will be ingested and transformed, in fact though `COPY` command we will access to the JSON files inside the buckets and copy their content on our staging tables.

## Database Schema Design

We have two staging tables which copy the JSON file inside the S3 buckets.

### Staging Tables

* staging_songs: information about songs and artists
* staging_events: actions done by users (which songs are listening, etc.. )

#### => Utilized a star schema optimized for queries on song play analysis

### Analytical tables
#### Fact Tables

* songplays: records event data associated with song plays including **songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent**. Since this fact table has **high cardinality** and **high join frequency**, the **distribution style** should be **KEY** and **distribution key** should be _"start_time"_ because of its high cardinality. Besides, the **sorting key** also should be _"start_time"_ because of its **high cardinality** so that it is easy for **filtering** tasks

#### Dimension Tables

* users: users in the app including **user_id, first_name, last_name, gender, level**. Since this dimension table does not have much data, the **distribution style** should be **ALL**. Besides, the _"user_id"_ should be **sorting key** due to its **high cardinality**
* songs: songs in music database including **song_id, title, artist_id, year, duration**. Since this dimension table does not have much data, the **distribution style** should be **ALL**. Besides, the _"year"_ should be **sorting key** due to its **high cardinality**
* artists: artists in music database including **artist_id, name, location, latitude, longitude**. Since this dimension table does not have much data, the **distribution style** should be **ALL**. Besides, the _"artist_id"_ should be **sorting key** due to its **high cardinality**
* time: timestamps of records in songplays broken down into specific units including **start_time, hour, day, week, month, year, weekday**. Since this dimension table has **high cardinality** and **high join frequency**, the **distribution style** should be **KEY** and **distribution key** should be _"start_time"_ because of its **high cardinality**. Besides, the **sorting key** also should be _"start_time"_ because of its **high cardinality** so that it is easy for **filtering** tasks

### Database Schema Design 

![Database Schema](images/schema.PNG)

### Data Warehouse Configurations and Setup

* Create a new `IAM user` in your AWS account
* Give it **AdministratorAccess** and **Attach policies**
* Use access key and secret key to create clients for `EC2`, `S3`, `IAM`, and `Redshift`.
* Create an `IAM Role` that makes `Redshift` able to access `S3 bucket` _(ReadOnly)_
* Create a `RedShift Cluster` and get the `DWH_ENDPOINT`_(Host address)_ and `DWH_ROLE_ARN` and fill the config file.

### ETL Pipeline

* Created tables to store the data from `S3 buckets`.
* Loading the data from `S3 buckets` to staging tables in the `Redshift Cluster`.
* Inserted data into fact and dimension tables from the staging tables.

### Project Structure

* `create_tables.py`: This script will drop old tables (if exist) and re-create new tables.
* `etl.py`: This script executes the queries that extract JSON data from the S3 bucket and ingest them to Redshift.
* `sql_queries.py`: This file contains variables with SQL statement in String formats, partitioned by CREATE, DROP, COPY and INSERT statement.
* `dhw.cfg`: Configuration file used that contains info about Redshift, IAM and S3

### How to Run

1. Create tables by running `create_tables.py`.
2. Execute ETL process by running `etl.py`.
