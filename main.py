#!/usr/bin/env python
"""
Geospatial Data Storage and Display (GeoDSD)

This program is a simple proof of concept and template of the following:

    a. Create and modify a SQLite database with geospatial data
    b. Create a user defined function to use in a SQL query
    c. Query database and save output to a Pandas dataframe
    d. Save query as a CSV
    e. Plot location(s) of query onto a map using matplotlib's basemap

Installation:
    All packages either come with a standard Python installation or are installable with pip or conda

Usage:
    $ python main.py

Input:
    1. CSV of fictious user metadata with lat/lons

Output:
    1. SQLite database file
    2. CSV of SQL query
    3. PNG image of map with location(s) of query results

The dataset used in this program is fictitious and does not intentionally reflect any real person
In Law & Order speak: "The preceding data is fictional. No actual person or event was depicted."

    This dataset created using:
    https://www.mockaroo.com

"""
# Import packages and modules
import sqlite3
import pandas as pd
from pygeocoder import Geocoder
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import os
import errno


# ~~~~ Specify Directory and File Paths ~~~~ #

# Location of CSV file to import into db as a table
csv_in = "./raw_data/user_meta_data.csv"

# Location and name of database to be created
db_dir = "./database/"
db_file = db_dir+"user_meta_data.db"

# Output directory
output_dir = "./output/"

# Name of CSV output file of SQL query
csv_out = output_dir + "query_results.csv"

# Name of PNG image of map of SQL query results
map_out = output_dir + "query_results.png"


# ~~~~ Functions ~~~~ #

def make_dir(path):
    """
    Function to check if output path exsists, and create directories as needed
    :param path: directory path
    :return: new directory if one does not previously exists

    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def findCountry(latitude, longitude):
    """
    Function to return country name based on latitude and longitude
    This function is initialized and used in the SQL query
    :param latitude: Latitude
    :param longitude: Longitutde
    :return: Country where latitude and longitude occurs

    """
    try:
        results = Geocoder.reverse_geocode(latitude, longitude)
        country_out = results.country
    except:
        # Since some lat lons do not belong to a country, we assign them NAN
        country_out = 'NAN'
    return country_out


def mapQuery(latitude, longitude, map_output_file):
    """
    Function takes in latitue and longitude and outputs a world map
    with location(s) of SQL queries
    :param latitude: Latitude
    :param longitude: Longitude
    :return: A PNG image in output directory of world map plot with locations of queried results

    """
    print("Plotting queried results...")
    bm = Basemap(projection='robin', resolution='l', area_thresh=1000.0, lat_0=0, lon_0=-130)
    bm.drawcoastlines()
    bm.drawcountries()
    bm.fillcontinents(color='lightgray')
    bm.drawmapboundary()
    bm.drawmeridians(np.arange(0, 360, 30))
    bm.drawparallels(np.arange(-90, 90, 30))

    for lon, lat in zip(longitude, latitude):
        x, y = bm(lon, lat)
        bm.plot(x, y, 'r*', markersize=10)

    plt.title("Location of Query Results")
    plt.savefig(map_output_file)
    print("Map of queried results: %s" % map_output_file)


def dbDriver(db_path, csv_input_file, csv_output_file, map_output_file):
    """
    Function that connects/creates to SQLite database,
    creates user defined SQL functions,
    executes SQL queries, and outputs a CSV file and PNG image of
    a map of the locations of the SQL query

    :param db_path: path to SQLite database
    :param csv_input_file: CSV file to create table from
    :param csv_output_file: CSV file to output query results
    :param map_output_file: PNG file with locations of query
    :return:

    """

    conn = sqlite3.connect(db_path)
    print("")
    print("Database created and opened succesfully: %s" % db_path)

    # Initialize functions used in queries
    conn.create_function("findCountry", 2, findCountry)

    # Load csv as pandas dataframe and then add (or replace) table to database
    print("Creating 'User Metadata' table from: %s\n" % csv_input_file)
    csv_df = pd.read_csv(csv_input_file)
    csv_df.to_sql("User Metadata", conn, flavor='sqlite', if_exists='replace')

    # SQL query
    print("Querying database...")
    print("Find where first name = Patrick \n")
    query_results = pd.read_sql_query("SELECT 'User Metadata'.[first_name] AS First_Name, "
                                      "'User Metadata'.[last_name] AS Last_Name, 'User Metadata'.[email] AS EMAIL, "
                                      "'User Metadata'.[lat] AS LATITUDE, 'User Metadata'.[lon] AS LONGITUDE, "
                                      "findCountry('User Metadata'.[lat], 'User Metadata'.[lon]) AS COUNTRY "
                                      "FROM 'User Metadata' WHERE (('User Metadata'.[first_name])=='Patrick')", conn)

    # Close database connection
    print("Query successful!")
    print("Closing database connection\n")
    conn.close()

    print("Generating outputs...")
    # Save SQL query as CSV in output directory
    query_results.to_csv(csv_output_file, index=False)
    print("CSV of queried results: %s" % csv_output_file)

    # Convert our data frame to a matrix for use with basemap in mapQuery function
    lat_array = query_results['LATITUDE'].as_matrix()
    lon_array = query_results['LONGITUDE'].as_matrix()

    # Call mapQuery function to plot our queried results
    mapQuery(lat_array, lon_array, map_output_file)


if __name__ == "__main__":
    print("\n~~ geoDSD now running ~~\n")
    print("Verifying all paths exist")
    make_dir(db_dir)
    make_dir(output_dir)
    dbDriver(db_file, csv_in, csv_out, map_out)
