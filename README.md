Geospatial Data Storage and Display (GeoDSD)
=========

About
--------
This program is a simple proof of concept and template of the following:

a. Create and modify a SQLite database with geospatial data  
b. Create a user defined function to use in a SQL query  
c. Query database and save output to a Pandas dataframe  
d. Save query as a CSV  
e. Plot location(s) of query onto a map using matplotlib's basemap  

### Plot locations of SQL query on map

![geoDSD dualmode](https://github.com/awentland90/geoDSD/blob/master/images/query_plot_results.png)


Download & Installation
--------

### Latest Code on GitHub

Use the following link to access the git repository:

*   **Git Repository:**

   The git repository can be found at: <https://github.com/awentland90/geoDSD>
   
    Get it using the following command:

        $ git clone git://github.com/awentland90/geoDSD.git

### Library & Package Dependencies
All packages either come with a standard Python installation or are installable with pip or conda

sqlite3  
pandas  
pygeocoder  
mpl_toolkits  
matplotlib  
numpy  
os  
errno  


Usage
--------

Usage:
$ python main.py

Input:
1. CSV of fictious user metadata with lat/lons

Output:
1. SQLite database file  
2. CSV of SQL query  
3. PNG image of map with location(s) of query results  
