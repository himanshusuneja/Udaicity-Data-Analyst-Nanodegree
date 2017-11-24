
# coding: utf-8

# In[45]:


'''

Since the data have been audited, cleaned and transfered into table and database, the following questions such as :
    
Number of nodes
Number of unique users
Number of ways
Most contributing users
Number of users who contributed only once
Top 10 amenities in New Delhi

Can be answered using following queries below

'''

import sqlite3
import csv

connect = sqlite3.connect("C:/Users/FAST/Desktop/Data Wrangling/Project 2/new-delhi_india.osm (1)_db.sqlite")
cursor = connect.cursor()

def number_of_nodes():
    result = cursor.execute('SELECT COUNT(*) FROM nodes')
    return result.fetchone()[0]

print 'Number of nodes: \n' , number_of_nodes()


def number_of_unique_users():
    result = cursor.execute('SELECT COUNT(DISTINCT e.uid) FROM                          
                            (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e')
                            
    return result.fetchone()[0]
                         
                           
print 'Number of unique users: \n' , number_of_unique_users() 



def number_of_ways():
    result = cursor.execute('SELECT COUNT(*) FROM ways')
    return result.fetchone()[0]

print 'Number of ways: \n' , number_of_ways()




def number_of_most_contributing_users():
    
    result = cursor.execute('SELECT e.user, COUNT(*) as num FROM                            
                            (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e            
                            GROUP BY e.user
                            ORDER BY num DESC
                            LIMIT 10')
                            
    return result.fetchall()                        
                            
                            
print 'Number of most contrubuting users: \n' , number_of_most_contributing_users()    


def number_of_users_contributing_only_once():
    result = cursor.execute('SELECT COUNT(*) FROM         
                            (SELECT e.user, COUNT(*) as num FROM     
                             (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e    
                             GROUP BY e.user                 
                             HAVING num = 1) u')
                            
    return result.fetchone()[0]
    
print 'Number of users contributing only once: \n' , number_of_users_contributing_only_once()    

def top_10_amenities():
    result = cursor.execute('SELECT value, COUNT(*) as num FROM nodes_tags          
                            WHERE key="amenity"                     
                            GROUP BY value                    
                            ORDER BY num DESC               
                            LIMIT 10')
                            
    return result.fetchall()

print 'Top 10 amenities: \n', top_10_amenities()

# Additional queries

## List of postalcodes

def list_of_postcodes():
    result = cursor.execute('SELECT e.value, COUNT(*) as num FROM     
                            (SELECT value FROM nodes_tags WHERE key="postcode"     
                             UNION ALL SELECT value FROM ways_tags WHERE key="postcode") e     
                            GROUP BY e.value                 
                            ORDER BY num DESC                     
                            LIMIT 10')
                            
    return result.fetchall()

print 'List of Postcodes: \n', list_of_postcodes()

## Specific address

def top_5_cusines():
    result = cursor.execute("SELECT nodes_tags.value, COUNT(*) as num               
                            FROM nodes_tags                         
                            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') AS restaurants    
                            ON nodes_tags.id = restaurants.id                       
                            WHERE nodes_tags.key = 'cuisine'                     
                            GROUP BY nodes_tags.value                      
                            ORDER BY num DESC                     
                            LIMIT 5")
                            
    return result.fetchall()

print 'Top 5 cusines: \n', top_5_cusines()




def top_5_banks():
    result = cursor.execute("SELECT nodes_tags.value, COUNT(*) as num        
                            FROM nodes_tags                       
                            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='bank') AS bank   
                            ON nodes_tags.id = bank.id              
                            WHERE nodes_tags.key = 'name'        
                            GROUP BY nodes_tags.value           
                            ORDER BY num DESC                 
                            LIMIT 5")
                            
    return result.fetchall()

print 'Top 5 banks: \n', top_5_banks()

