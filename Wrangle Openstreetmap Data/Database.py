
# coding: utf-8

# In[1]:


# This file created SQL Tables for nodes, nodes_tags, wasy, ways_tags and ways_nodes

import sqlite3
import csv
from pprint import pprint

sqlite_file = 'new-delhi_india.osm (1)_db.sqlite'

# Connecting to the database
connect = sqlite3.connect(sqlite_file)
connect.text_factory = str
cursor = connect.cursor()

# create nodes table
cursor.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp);")

with open('nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp'])              for i in dr]

cursor.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp)                 VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
connect.commit()

# create nodes_tags table
cursor.execute("CREATE TABLE nodes_tags (id, key, value, type);")

with open('nodes_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]
    
# Inserting Data
cursor.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)

connect.commit()

# Create ways table
cursor.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")

with open('ways.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

# Inserting Data
cursor.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)

connect.commit()

# Create ways_nodes table
cursor.execute("CREATE TABLE ways_nodes (id, node_id, position);")

with open('ways_nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

# Inserting Data
cursor.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db)

connect.commit()

# Create ways_tags table
cursor.execute("CREATE TABLE ways_tags (id, key, value, type);")

with open('ways_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

# Inserting Data
cursor.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)

connect.commit()

